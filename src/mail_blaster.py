import logging
import smtplib
from typing import List
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailBlaster():

    _FROM_EMAIL_ADDRESS = str("arnie@FlowerBox.com")

    _logger = logging.getLogger(__name__)
    _addresses = None
    _smpt = None

    def __init__(self, addresses: List[str], smpt: smtplib.SMTP = None):
        if addresses is None:
            raise TypeError
        self._addresses = addresses
        self._smpt = smpt or smtplib.SMTP('localhost')

    def sendMessage(self, message: str, subject: str):
        for e in self._addresses:
            try:
                msg = MIMEMultipart()
                msg['From'] = self._FROM_EMAIL_ADDRESS
                msg['To'] = e
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))

                self._smpt.sendmail(msg=msg.as_string(), to_addrs=e, from_addr=self._FROM_EMAIL_ADDRESS)
            except smtplib.SMTPException:
                self._logger.warn('Unable to send email to: [{}]'.format(e))
