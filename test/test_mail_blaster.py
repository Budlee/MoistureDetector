import builtins
import smtplib
import unittest
from unittest.mock import Mock

import mock

import context
from src.mail_blaster import MailBlaster


class TestMailSender(unittest.TestCase):

    _EMAIL_ADDRESS_1 = str('xyz@xyz.com')
    _EMAIL_ADDRESS_2 = str('zyx@zyx.com')
    _addresses = None
    _mailSender = None
    _mockSmpt = None

    def setUp(self):
        self._mockSmpt = Mock(spec_set=smtplib.SMTP)
        self._addresses = [self._EMAIL_ADDRESS_1, self._EMAIL_ADDRESS_2]
        self._mailSender = MailBlaster(self._addresses, self._mockSmpt)

    def test_addresses_can_not_be_none(self):
        with self.assertRaises(TypeError):
            MailBlaster(None)

    def test_all_email_addresses_are_sent_to(self):
        self._mailSender.sendMessage("message", "subject")
        self._mockSmpt.sendmail.assert_any_call(
            msg=mock.ANY, to_addrs=self._EMAIL_ADDRESS_1, from_addr=mock.ANY)
        self._mockSmpt.sendmail.assert_any_call(
            msg=mock.ANY, to_addrs=self._EMAIL_ADDRESS_2, from_addr=mock.ANY)

    def test_all_email_addresses_are_sent_to_if_excepion_is_thrown(self):
        rubbishEmail = str('RUBBISH')

        def side_effect(*args, **kwargs):
            if kwargs['to_addrs'] == rubbishEmail:
                raise smtplib.SMTPException
            return mock.DEFAULT

        attrs = {'sendmail.side_effect': side_effect}
        self._mockSmpt = Mock(spec_set=smtplib.SMTP, **attrs)
        self._addresses = [self._EMAIL_ADDRESS_1,
                           rubbishEmail, self._EMAIL_ADDRESS_2]
        self._mailSender = MailBlaster(self._addresses, self._mockSmpt)
        self._mailSender.sendMessage("message", "subject")
        self._mockSmpt.sendmail.assert_any_call(
            msg=mock.ANY, to_addrs=self._EMAIL_ADDRESS_1, from_addr=mock.ANY)
        self._mockSmpt.sendmail.assert_any_call(
            msg=mock.ANY, to_addrs=self._EMAIL_ADDRESS_2, from_addr=mock.ANY)

    def test_from_email_address_is_used_to_send_email(self):
        self._mailSender.sendMessage("message", "subject")
        self._mockSmpt.sendmail.assert_any_call(
            msg=mock.ANY, to_addrs=mock.ANY, from_addr='arnie@FlowerBox.com')

    def test_message_passed_is_sent_out(self):
        messageBody = str('Message Body Text')
        caughtArguments = list()

        def side_effect(*args, **kwargs):
            caughtArguments.append(kwargs['msg'])
            return mock.DEFAULT

        self._mockSmpt.sendmail.side_effect = side_effect
        self._mailSender = MailBlaster(self._addresses, self._mockSmpt)
        self._mailSender.sendMessage(messageBody, "subject")

        for m in caughtArguments:
            self.assertIn(messageBody, m)

    @mock.patch('smtplib.SMTP')
    def test_subject_passed_is_sent_out(self, mock_smtp):
        subject = str('Super Subject')
        caughtArguments = list()

        def side_effect(*args, **kwargs):
            caughtArguments.append(kwargs['msg'])
            return mock.DEFAULT

        self._mockSmpt.sendmail.side_effect = side_effect
        self._mailSender = MailBlaster(self._addresses, self._mockSmpt)
        self._mailSender.sendMessage("", subject)

        for s in caughtArguments:
            self.assertIn('Subject: Super Subject', s)
