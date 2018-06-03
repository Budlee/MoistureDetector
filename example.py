#!/usr/bin/python3

import time
from src.mail_blaster import MailBlaster
from src.moisture_detector import MoistureDetector


def main():
    mail_blaster = MailBlaster(addresses=['example@example.com'])
    moisture_detector = MoistureDetector(17, mail_blaster)
    moisture_detector.start()
    while True:
        time.sleep(0.1)


if __name__ == '__main__':
    main()
