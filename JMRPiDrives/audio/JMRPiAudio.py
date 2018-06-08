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
# RPi Spark Audio Device
#
# Author: Kunpeng Zhang
# 2018.4.15
#

import subprocess as sub
PIN_MODE_AUDIO = "alt0"
PIN_MODE_OUTPUT = "output"

class SSAudioDevice:
    channelR = None
    channelL = None
    
    def __init__(self, pinRight, pinLeft):
        self.channelR = pinRight
        self.channelL = pinLeft

    # Open Audio output. set pin mode to ALT0
    def on(self):
        isOK = True
        try:
            if self.channelR!=None:
                sub.call(["gpio", "-g", "mode", "{}".format(self.channelR), PIN_MODE_AUDIO ])
        except:
            isOK = False
            print("Open audio right channel failed.")

        try:
            if self.channelL!=None:
                sub.call(["gpio","-g","mode", "{}".format(self.channelL), PIN_MODE_AUDIO ])
        except:
            isOK = False
            print("Open audio left channel failed.")

        return isOK
    
    # Close Audio output. set pin mode to OUTPUT
    def off(self):
        isOK = True
        try:
            if self.channelR!=None:
                sub.call(["gpio","-g","mode", "{}".format(self.channelR), PIN_MODE_OUTPUT ])
        except:
            isOK = False
            print("Close audio right channel failed.")

        try:
            if self.channelL!=None:
                sub.call(["gpio","-g","mode", "{}".format(self.channelL), PIN_MODE_OUTPUT ])
        except:
            isOK = False
            print("Close audio left channel failed.")
        return isOK