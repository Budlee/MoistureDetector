import unittest
import mock
import context
import RPi.GPIO

from src.mail_blaster import MailBlaster
from src.moisture_detector import MoistureDetector


class TestMoistureDetector(unittest.TestCase):

    _INPUT_PIN = int(17)

    _mock_mail_blaster = None
    _mock_GPIO = None
    _md = None

    def setUp(self):
        self._mock_mail_blaster = mock.Mock(spec_set=MailBlaster)
        patch = mock.patch('RPi.GPIO')
        self._mock_GPIO = patch.start()
        self.addCleanup(patch.stop)
        self._md = MoistureDetector(self._INPUT_PIN, self._mock_mail_blaster)

    def test_GPIO_uses_passed_in_pin_for_sensor(self):
        self._mock_GPIO.reset_mock()
        pin = int(10)
        md = MoistureDetector(pin, self._mock_mail_blaster)
        self._mock_GPIO.setup.assert_called_once_with(pin, RPi.GPIO.IN)

    def test_GPIO_pin_detection_added(self):
        self._md.start()
        self._mock_GPIO.add_event_detect.assert_called_once_with(
            self._INPUT_PIN, RPi.GPIO.BOTH, bouncetime=mock.ANY)

    def test_email_sent_when_water_is_low(self):
        self._md.start()
        self._md._sensor_callback(self._INPUT_PIN)
        self._mock_GPIO.input.return_value = [False, True, False]
        self._mock_mail_blaster.sendMessage.assert_called_once_with(
            "The flower boxes are low on water", "9000 water boxes")

    def test_start_registers_callback_for_sensor(self):
        self._md.start()
        self._mock_GPIO.add_event_callback.assert_called_once_with(
            self._INPUT_PIN, mock.ANY)
        args = self._mock_GPIO.add_event_callback.call_args
        self.assertTrue(callable(args[0][1]))

    def test_setup_called_before_detect_for_GPIO(self):
        self._mock_GPIO.reset_mock()
        self._md = MoistureDetector(self._INPUT_PIN, self._mock_mail_blaster)
        calls = [mock.call.setup(mock.ANY, mock.ANY),
                 mock.call.add_event_detect(mock.ANY, mock.ANY, bouncetime=mock.ANY)]
        self._mock_GPIO.assert_has_calls(calls)
