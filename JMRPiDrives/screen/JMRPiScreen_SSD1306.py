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
#    RPi Spark SSD1306Screen
#    by Kunpeng Zhang
#    v1.0.0
#
#    Using SSD1306 chip-driven OLED display
#    使用 SSD1306 芯片驱动的 OLED 显示屏
#

from .JMRPiSSPILScreen import SSPILScreen

class SScreenSSD1306( SSPILScreen ):
    """This class work with PIL Lib.
    """

    def __init__(self, display, bufferColorMode, bufferSize=None, displayDirection=0 ):
        self._checkBufferColorMode(bufferColorMode)
        # Initialize display.
#         display.begin()
        self._screen_color_mode = "1"
        self._initDisplay(display, displayDirection, (display.width, display.height))

        # Initialize buffer and canvas
        self._initBuffer( bufferColorMode, bufferSize )
        pass

    def refresh(self):
        """Update current view content to display
        """

        try:
            # suport for JMRPiDisplay SSD1306 driver
            self.Display.setImage( self._catchCurrentViewContent() )
        except:
            try:
                # suport for Adafruit SSD1306 driver
                self.Display.image( self._catchCurrentViewContent() )
            except:
                raise "Can not update image to buffer."

        self.Display.display()
        pass

    def clear(self):
        """Clear display and screen's canvas
        """
        self.clearCanvas()
        self.Display.clear()
        pass

    pass