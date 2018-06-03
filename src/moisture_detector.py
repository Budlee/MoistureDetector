from src.mail_blaster import MailBlaster
import RPi.GPIO


class MoistureDetector():

    _mail_blaster = None
    _channel = None

    def __init__(self, channel : int, mail_blaster : MailBlaster):
        self._channel = channel
        self._mail_blaster = mail_blaster
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(channel, RPi.GPIO.IN)
        RPi.GPIO.add_event_detect(channel, RPi.GPIO.BOTH, bouncetime=300)

    def _sensor_callback(self, channel : int):
        if RPi.GPIO.input(channel):
            self._mail_blaster.sendMessage("The flower boxes are low on water", "9000 water boxes")
    
    def start(self):
        RPi.GPIO.add_event_callback(self._channel, self._sensor_callback)