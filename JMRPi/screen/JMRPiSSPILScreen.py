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
#    RPi Spark PILScreen
#    by Kunpeng Zhang
#    v1.0.0
#    
#    Use PIL as cache for draw canvas
#    使用 PIL 作为绘制缓存的显示屏实现
#
import types

import PIL
from PIL import Image
from PIL import ImageDraw

import JMRPiScreenBase

class SSPILScreen( JMRPiScreenBase.SScreenBase ):
    """This class work with PIL Image Lib.
    """

    def _catchCurrentViewContent(self):
        viewContent = None
        if self._buffer_color_mode != self._display_color_mode:
            viewContent = self._buffer.crop( self.View.rectToArray() ) .convert( self._display_color_mode )
        else:
            viewContent = self._buffer.crop( self.View.rectToArray() )

        # Rotate for display direction
        if self._display_direction == 0:
            return viewContent
        else:
            return viewContent.rotate( angle = self._display_direction, expand=True )
        pass

    def _initBuffer(self, bufferColorMode, bufferSize):
        # super(SSScreenBase)._initBuffer(bufferColorMode, bufferSize)
        self._buffer_color_mode = bufferColorMode

        #create screen image buffer and canvas
        if bufferSize==None:
            self._buffer = Image.new( bufferColorMode , self._display_size )
        else:
            self._buffer = Image.new( bufferColorMode , bufferSize )        
        self.Canvas = ImageDraw.Draw( self._buffer )

        #creare screen view
        self.View = JMRPiScreenBase.SSRect( 0, 0, self._display_size[0], self._display_size[1] )
        pass

    def getBufferSize(self):
        return self._buffer.size
        pass

#     def refresh(self):
#         """Update current view content to display
#         """
#         pass

    def clearCanvas(self, fillColor = 0 ):
        self.Canvas.rectangle((0, 0, self._display_size[0], self._display_size[1]), outline=0, fill=fillColor)
        pass
    
    def clearView(self, fillColor = 0 ):
        self.Canvas.rectangle(self.View.rectToArray(), outline=0, fill=fillColor)

    def clear(self):
        """Clear display and screen's canvas
        """
        self.clearCanvas()
        self.Display.clear()
        pass

    def redefineBuffer(self, newBuffer ):
        """Redefine buffer of display newBuffer maybe is image or Dict{ "size"=(width, height), "colorMode"="1" or "RGB" }
        """
        # Redefine Frame from an image object
        if type(self._buffer) == type(newBuffer):
            self._buffer = newBuffer
            self.Canvas = ImageDraw.Draw( self._buffer )
            return True
        
        # Redefine Frame from an <PIL.ImageFile.ImageFile>
        if type(newBuffer).__name__.find(PIL.ImageFile.ImageFile.__name__) != -1:        
            self._buffer = self._buffer.resize((newBuffer.width, newBuffer.height))
            self._buffer.paste( newBuffer, (0,0))
            return True

        # Recreated a new frame from dict of frame
        if isinstance(newBuffer, {}):
            self._buffer = Image.new( newBuffer["colorMode"] , newBuffer["size"] )
            self.Canvas = ImageDraw.Draw( self._buffer )
            return True
        pass

    pass