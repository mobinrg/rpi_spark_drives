# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2018 Kunpeng Zhang
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# #########################################################
#
# RPi Spark Shield -- Key Buttons
# Keyboard include Joystick buttons and Action buttons, 
# keyboard use BCM mode, there are keyboard layout:
# 
#              [JOY UP]
# [JOY LEFT]   [JOY OK]   [JOY RIGHT]             [ACT_A]  [ACT_B]
#              [JOY DOWN]
#
# Kunpeng Zhang
# v1.0    2018.3.8
#

import RPi.GPIO as GPIO

# Action Buttons    BCM_IO_NUM
BUTTON_ACT_A        = 22
BUTTON_ACT_B        = 23

# Joy Buttons       BCM_IO_NUM
BUTTON_JOY_LEFT     = 26
BUTTON_JOY_RIGHT    = 27
BUTTON_JOY_UP       = 5
BUTTON_JOY_DOWN     = 6
BUTTON_JOY_OK       = 24

DEF_BOUNCE_TIME_SHORT_MON    = 10
DEF_BOUNCE_TIME_SHORT    = 50
DEF_BOUNCE_TIME_NORMAL   = 100
DEF_BOUNCE_TIME_LONG     = 200

#SparkKeyboard
class SSKeyButtons :
    """This RPi Spark Shield -- Key Buttons Drive
    """
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        pass

    def setKeyButton( self, btnID, keyCallback, bounceTime = DEF_BOUNCE_TIME_NORMAL, pullUpDown = GPIO.PUD_UP, event = GPIO.BOTH ):
        """Set key button event
        btnID: key pin number in BCM
        keyCallback: interrupt callback function, if has set to None mean is keybutton work in query mode
        bounceTime: default DEF_BOUNCE_TIME_NORMAL
        pullUpDown: default set to GPIO.PUD_UP
        event: default set to GPIO.RISING. it can be { RISING, FALLING, BOTH }
        """
        GPIO.setup( btnID, GPIO.IN, pull_up_down=pullUpDown)
        # The keyCallback is None mean is setting keybutton in query mode, 
        # then uses readKeyButton for get keybutton status
        # event can be { RISING, FALLING, BOTH }
        if keyCallback != None:
            try:
                GPIO.add_event_detect( btnID, event, callback=keyCallback, bouncetime=bounceTime )
            except:
                pass
        pass

    def setKeyButtonCallback(self, btnID, keyCallback):
        GPIO.add_event_callback( btnID, keyCallback )

    def removeKeyButtonEvent(self, buttons= [] ):
        for i in range( 0, len(buttons)-1 ):
            GPIO.remove_event_detect( buttons[i] )

    def readKeyButton( self, btnID ):
        return GPIO.input(btnID)

    def configKeyButtons( self, enableButtons = [], bounceTime = DEF_BOUNCE_TIME_NORMAL, pullUpDown = GPIO.PUD_UP, event = GPIO.BOTH ):
        """enableButtons = [{ "id":BUTTON_ACT_A, "callback": aCallbackFun }, ... ]
        """
        for key in enableButtons:
            self.setKeyButton( key["id"], key["callback"], bounceTime, pullUpDown, event )
        pass
