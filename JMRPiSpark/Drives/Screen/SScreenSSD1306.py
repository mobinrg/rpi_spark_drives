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
#    RPi-Spark SSD1306Screen
#    by Kunpeng Zhang
#    v1.0.0
#
#    Using SSD1306 chip-driven OLED display
#    使用 SSD1306 芯片驱动的 OLED 显示屏

from .SSPILScreen import SSPILScreen

class SScreenSSD1306( SSPILScreen ):
    """!
    \~english
    Using SSD1306 chip to implement the SScreen object
    Supported: JMRPiDisplay SSD1306 driver and Adafruit SSD1306 driver

    \~chinese
    使用 SSD1306 显示芯片实现的 SScreen 对象
    支持: JMRPiDisplay_SSD1306 和 Adafruit SSD1306 driver
    """
    def __init__(self, display, bufferColorMode, bufferSize=None, displayDirection=0 ):
        """!
        \~english
        Initialize the SScreenSSD1306 object instance
        @param display: a display hardware instance, eg. SSD1306
        @param bufferColorMode: color mode, can be chosen: SS_COLOR_MODE_MONO ("1") or SS_COLOR_MODE_RGB ("RGB")
        @param bufferSize: size of buffer, eg. (128,64) or (320, 240) ...
        @param displayDirection: direction of display, can be: 0, 90, 180, 270
        
        \~chinese
        初始化 SScreenSSD1306 对象实例
        @param display: 显示屏硬件对象实例，例如： SSD1306
        @param bufferColorMode: 缓存色彩模式，取值： SS_COLOR_MODE_MONO ("1") 或 SS_COLOR_MODE_RGB ("RGB")
        @param bufferSize: 缓存大小，例如： (128,64) or (320, 240) ...
        @param displayDirection: 显示屏方向，取值：0, 90, 180, 270
        """
        self._checkBufferColorMode(bufferColorMode)
        # Initialize display.
#         display.begin()
        self._display_color_mode = "1"
        self._initDisplay(display, displayDirection, (display.width, display.height))

        # Initialize buffer and canvas
        self._initBuffer( bufferColorMode, bufferSize )

    def refresh(self):
        """!
        \~english
        Update current view content to display
        Supported: JMRPiDisplay_SSD1306 and Adafruit SSD1306 driver

        \~chinese
        更新当前视图内容到显示屏
        支持: JMRPiDisplay_SSD1306 和 Adafruit SSD1306 driver
        """
        try:
            # suport for RPiDisplay SSD1306 driver
            self.Display.setImage( self._catchCurrentViewContent() )
        except:
            try:
                # suport for Adafruit SSD1306 driver
                self.Display.image( self._catchCurrentViewContent() )
            except:
                raise "Can not update image to buffer."

        self.Display.display()