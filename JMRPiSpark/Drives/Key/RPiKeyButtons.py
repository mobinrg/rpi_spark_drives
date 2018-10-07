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
# RPi-Spark pHAT -- Key Buttons
# Keyboard include Joystick buttons and Action buttons, 
# keyboard use BCM mode, there are keyboard layout:
# 
#              [JOY UP]
# [JOY LEFT]   [JOY OK]   [JOY RIGHT]             [ACT_A]  [ACT_B]
#              [JOY DOWN]
#
# @author Kunpeng Zhang
# v1.0    2018.3.8
#

import RPi.GPIO as GPIO

# Action Buttons    BCM_IO_NUM
# BUTTON_ACT_A        = 22
# BUTTON_ACT_B        = 23

# Joy Buttons       BCM_IO_NUM
# BUTTON_JOY_LEFT     = 26
# BUTTON_JOY_RIGHT    = 27
# BUTTON_JOY_UP       = 5
# BUTTON_JOY_DOWN     = 6
# BUTTON_JOY_OK       = 24

# UNIT: ms
DEF_BOUNCE_TIME_SHORT_MON   = 10
DEF_BOUNCE_TIME_SHORT       = 50
DEF_BOUNCE_TIME_NORMAL      = 100
DEF_BOUNCE_TIME_LONG        = 200

#SparkKeyboard
class RPiKeyButtons :
    """!
    \~english This RPi-Spark pHAT Key Buttons Drive
    \~chinese 树梅派火花(RPi-Spark pHAT) 按键驱动
    """
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        pass

    def setKeyButton( self, btnId, keyCallback, bounceTime = DEF_BOUNCE_TIME_NORMAL, pullUpDown = GPIO.PUD_UP, event = GPIO.BOTH ):
        """!
        \~english
        Set key button event
        @param btnId: Key button pin number in BCM
        @param keyCallback: A interrupt <b>callback_function</b> or <b>None</b>. <br>
               If set to <b>None</b> means keybutton work in query mode<br>
               then uses RPiKeyButtons#readKeyButton for get keybutton status
        @param bounceTime: Default set to DEF_BOUNCE_TIME_NORMAL
        @param pullUpDown: Default set to GPIO.PUD_UP
        @param event: Default set to GPIO.BOTH. it can be: { GPIO.RISING | GPIO.FALLING | GPIO.BOTH }

        \~chinese
        设置按键事件
        @param btnId: 按键IO号(in BCM mode)
        @param keyCallback: 按键中断回调函数 <b>callback_function</b> 或 <b>None</b><br>
                如果设置为<b>None</b>，则表示按键工作在查询模式<br>
                然后使用 RPiKeyButtons#readKeyButton 获取 keybutton 状态
        @param bounceTime: 默认 DEF_BOUNCE_TIME_NORMAL
        @param pullUpDown: 默认 GPIO.PUD_UP
        @param event: 默认 GPIO.BOTH 它可以是: { GPIO.RISING | GPIO.FALLING | GPIO.BOTH }

        \~ \n
        @see DEF_BOUNCE_TIME_SHORT_MON (10ms)
        @see DEF_BOUNCE_TIME_SHORT (50ms)
        @see DEF_BOUNCE_TIME_NORMAL (100ms)
        @see DEF_BOUNCE_TIME_LONG (200ms)

        @note
            * setKeyButton(btnId = 12, keyCallback = None )
            * setKeyButton(btnId = 14, keyCallback = aKeyCallbackFun ) <br>
                <pre>
                \# a simple callback function
                def aKeyCallbackFun(channel):
                    print(channel)
                    pass
                </pre>
        """
        GPIO.setup( btnId, GPIO.IN, pull_up_down=pullUpDown)
        # The keyCallback is None means setting keybutton in query mode, 
        # then uses readKeyButton for get keybutton status
        # event can be { RISING, FALLING, BOTH }
        if keyCallback != None:
            try:
                GPIO.add_event_detect( btnId, event, callback=keyCallback, bouncetime=bounceTime )
            except:
                pass
        pass

    def setKeyButtonCallback(self, btnId, keyCallback):
        """!
        \~english
        Set key button event callback
        @param btnId: button id number of GPIO. eg. 13 or 15 etc.
        @param keyCallback: a callback function. eg.\n
        \~chinese
        设置按键事件回调
        @param btnId: 按键IO号(in BCM mode) 例如: 13 or 15 etc.
        @param keyCallback: 回调函数 例如:\n
        \~
        <pre>
        def keyCallback(channel):
           print(channel)
           pass
        </pre>
        """
        GPIO.add_event_callback( btnId, keyCallback )

    def removeKeyButtonEvent(self, buttons= [] ):
        """!
        \~english
        Remove key button event callbacks
        @param buttons: an array of button Ids. eg. [ 12,13,15, ...]

        \~chinese
        移除按键事件回调
        @param buttons: 按钮ID数组。 例如: [12,13,15，...]
        """
        for i in range( 0, len(buttons)-1 ):
            GPIO.remove_event_detect( buttons[i] )

    def readKeyButton( self, btnId ):
        """!
        \~english
        Read an button IO status
        @return an boolean value
        \~chinese
        读取按钮IO状态
        @return 布尔值
        """
        return GPIO.input(btnId) if btnId != None else False

    def configKeyButtons( self, enableButtons = [], bounceTime = DEF_BOUNCE_TIME_NORMAL, pullUpDown = GPIO.PUD_UP, event = GPIO.BOTH ):
        """!
        \~english
        Config multi key buttons IO and event on same time

        @param enableButtons: an array of key button configs. eg. <br>
                [{ "id":BUTTON_ACT_A, "callback": aCallbackFun }, ... ]
        @param bounceTime: Default set to DEF_BOUNCE_TIME_NORMAL
        @param pullUpDown: Default set to GPIO.PUD_UP
        @param event: Default set to GPIO.BOTH. it can be: { GPIO.RISING | GPIO.FALLING | GPIO.BOTH }

        \~chinese
        同时配置多个按键IO和事件

        @param enableButtons: 组按键配置 例如: <br>
                [{ "id":BUTTON_ACT_A, "callback": aCallbackFun }, ... ]
        @param bounceTime: 默认 DEF_BOUNCE_TIME_NORMAL
        @param pullUpDown: 默认 GPIO.PUD_UP
        @param event: 默认 GPIO.BOTH 它可以是: { GPIO.RISING | GPIO.FALLING | GPIO.BOTH }

        \~ \n
        @see DEF_BOUNCE_TIME_SHORT_MON (10ms)
        @see DEF_BOUNCE_TIME_SHORT (50ms)
        @see DEF_BOUNCE_TIME_NORMAL (100ms)
        @see DEF_BOUNCE_TIME_LONG (200ms)
        """
        for key in enableButtons:
            self.setKeyButton( key["id"], key["callback"], bounceTime, pullUpDown, event )
        pass
