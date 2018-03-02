#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import datenbank

card1=[144, 171, 217, 217, 59]
card2=[76, 156, 217, 217, 208]
card3=[198, 19, 218, 217, 214]


continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print ("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
       print ("card detected")
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    
    if card1 == uid:
        print(uid)
        time.sleep(1)
    if card2 == uid:
        print(uid)
        time.sleep(1)
    if card3 == uid:
        print(uid)
        time.sleep(1)


