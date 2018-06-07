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
#    RPi Spark ScreenBase
#    by Kunpeng Zhang
#    v1.0.0
#

# Display color mode
SS_COLOR_MODE_MONO  = "1"
SS_COLOR_MODE_RGB   = "RGB"

class SSPoint:
    x = 0
    y = 0
    pass

class SSRect:
    x       = 0
    y       = 0
    height  = 0
    width   = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        pass

    def resize(self, newWidth = 0, newHeight = 0):
        self.height = newHeight
        self.width = newWidth
        pass

    def adjuestSize(self, offsetWidth = 0, offsetHeight = 0):
        self.height += offsetHeight
        self.width += offsetWidth
        pass

    def moveTo(self, newX=0, newY=0):
        self.x = newX
        self.y = newY
        pass
    
    def moveOffset(self, offsetX=0, offsetY=0):
        self.x += offsetX
        self.y += offsetY
        pass
    
    def swapWH(self):
        """Swap width and height of rect
        """
        width = self.width
        self.width = self.height
        self.height = width
        pass

    def rectToArray(self, swapWH = False):
        if swapWH == False:
            return [self.x, self.y, self.x + self.width, self.y + self.height]
        else:
            return [self.x, self.y, self.x + self.height, self.y + self.width]
        pass

    pass

class SScreenBase:
    Display = None
    Canvas = None
    View = None

    # Display direction can choos in 0, 90, 180, 270
    _display_direction = 0
    # Display's size, it init at intance when __init__ (x,y), and it keep same direction whit "_display_direction"
    # If you need to access the physical size, use the “Display” object
    _display_size = (0,0)
    # "1": greyscale or "RGB" : image
    _display_color_mode = SS_COLOR_MODE_MONO
    _buffer_color_mode = SS_COLOR_MODE_MONO
    # Screen buffer
    _buffer = None

    def __init__(self, display, bufferColorMode, bufferSize=None, displayDirection=0 ):pass
    
    def _initDisplay(self, display, displayDirection, displaySize=(0,0)):
        self._display_direction = displayDirection
        
        if self._needSwapWH():
            self._display_size = ( displaySize[1], displaySize[0] )
        else:
            self._display_size = displaySize

        self.Display = display
        pass

    def _initBuffer(self, bufferColorMode, bufferSize):
        self._buffer_color_mode = bufferColorMode
        pass
    
    def _needSwapWH(self):
        return (self._display_direction != 0 and self._display_direction != 180 )

    def _checkBufferColorMode(self, bufferColorMode):
        if bufferColorMode != SS_COLOR_MODE_RGB and bufferColorMode != SS_COLOR_MODE_MONO:
            raise ValueError("Incorrect bufferColorMode mode, this value just choose in: \"RGB\" and \"1\" ")
        pass

    def refresh(self):
        """Update current view content to display
        """
        pass

    def clear(self):
        """Clear display
        """
        pass

    def redefineBuffer(self, newFrame ):
        """Redefine frame of Screen
        newFrame maybe is Image or Dict{ "size", "colorMode", etc. }
        """
        pass
    
    def changeBufferColorMode(self, newColorMode = SS_COLOR_MODE_MONO):
        """Change buffer color mode
        newColorMode can be choose { SS_COLOR_MODE_MONO | SS_COLOR_MODE_RGB }
        """
        self._initBuffer(newColorMode, None)

    def getDisplaySize(self):
        return self._display_size

    def getBufferSize(self):pass
    pass