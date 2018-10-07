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
# RPi-Spark Audio Device
#
# @author: Kunpeng Zhang
# 2018.4.15
#

import subprocess as sub

class RPiAudioDevice:
    PIN_MODE_AUDIO = "alt0"
    PIN_MODE_OUTPUT = "output"

    ##
    # Audio right channel IO
    channelR = None
    ##
    # Audio left channel IO
    channelL = None
    
    def __init__(self, pinRight, pinLeft):
        """!
        \~english
        Initialize the RPiAudioDevice object instance.
        @param pinRight: Audio right channel IO. "None" means channel disabled
        @param pinLeft: Audio left channel IO. "None" means channel disabled
        @note On Raspberry Pi the audio channel IO can be chosen in ( GPIO in BCM MODE ): 12, 13, 18
        
        \~chinese
        初始化 RPiAudioDevice 对象实例。
        @param pinRight: 音频右声道 IO 。 "None" 表示通道禁用
        @param pinLeft: 音频左声道 IO 。 "None" 表示通道禁用
        @note 树梅派(Raspberry Pi)可选择音频通道输出 IO（BCM 模式）：12,13,18            
        """
        self.channelR = pinRight
        self.channelL = pinLeft
 
    def on(self):
        """!
        \~english
        Open Audio output. set pin mode to ALT0
        @return a boolean value. if True means open audio output is OK otherwise failed to open.

        \~chinese
        打开音频输出。 将引脚模式设置为ALT0
        @return 布尔值。 如果 True 表示打开音频输出成功，否则不成功。
        """
        isOK = True
        try:
            if self.channelR!=None:
                sub.call(["gpio", "-g", "mode", "{}".format(self.channelR), self.PIN_MODE_AUDIO ])
        except:
            isOK = False
            print("Open audio right channel failed.")

        try:
            if self.channelL!=None:
                sub.call(["gpio","-g","mode", "{}".format(self.channelL), self.PIN_MODE_AUDIO ])
        except:
            isOK = False
            print("Open audio left channel failed.")

        return isOK
    
    # Close Audio output. set pin mode to OUTPUT
    def off(self):
        """!
        \~english
        Close Audio output. set pin mode to output
        @return a boolean value. if True means close audio output is OK otherwise failed to close.

        \~chinese
        关闭音频输出。 将引脚模式设置为输出
        @return 布尔值。 如果为 True 关闭音频输出成功，否则关闭不成功。
        """
        isOK = True
        try:
            if self.channelR!=None:
                sub.call(["gpio","-g","mode", "{}".format(self.channelR), self.PIN_MODE_OUTPUT ])
        except:
            isOK = False
            print("Close audio right channel failed.")

        try:
            if self.channelL!=None:
                sub.call(["gpio","-g","mode", "{}".format(self.channelL), self.PIN_MODE_OUTPUT ])
        except:
            isOK = False
            print("Close audio left channel failed.")
        return isOK