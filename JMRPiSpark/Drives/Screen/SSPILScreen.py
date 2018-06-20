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

from .SScreen import SScreenBase
from .SScreen import SSRect

class SSPILScreen( SScreenBase ):
    """!
    \~english This class work with PIL Image Lib.
    \~chinese 使用 PIL 库实现的 SScreen 类
    """

    def _catchCurrentViewContent(self):
        """!
        \~english
        Catch the current view content
        @return: a PIL Image
        @note 
            Automatically converts the cache color mode and at the 
            same time rotates the captured image data according to 
            the screen angle

        \~chinese
        从缓存中抓取当前视图大小的数据
        @return: PIL Image 对象
        @note 自动转换缓存色彩模式，同时根据屏幕角度设定旋转所抓取的图像数据
        """
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

    def _initBuffer(self, bufferColorMode, bufferSize):
        """!
        \~english
        Initialize the buffer object instance, use PIL Image as for buffer
        @param bufferColorMode: "RGB" or "1"
        @param bufferSize: (width, height)
        \~chinese
        初始化缓冲区对象实例，使用PIL Image作为缓冲区
        @param bufferColorMode: 色彩模式, 取值： "RGB" 或 "1"
        @param bufferSize: 缓存大小 (width, height)，例如： (128, 64)
        """
        # super(SSScreenBase)._initBuffer(bufferColorMode, bufferSize)
        self._buffer_color_mode = bufferColorMode

        #create screen image buffer and canvas
        if bufferSize==None:
            self._buffer = Image.new( bufferColorMode , self._display_size )
        else:
            self._buffer = Image.new( bufferColorMode , bufferSize )        
        self.Canvas = ImageDraw.Draw( self._buffer )

        #creare screen view
        self.View = SSRect( 0, 0, self._display_size[0], self._display_size[1] )

    def getBufferSize(self):
        return self._buffer.size

#     def refresh(self):
#         """Update current view content to display
#         """
#         pass

    def clearCanvas(self, fillColor = 0 ):
        """!
        \~engliash
        Clear up canvas and fill color at same time
        @param fillColor:  a color value
        @note 
            The fillColor value range depends on the setting of _buffer_color_mode.
            * If it is SS_COLOR_MODE_MONO ("1") monochrome mode, it can only select 0: black and 1: white
            * If it is SS_COLOR_MODE_RGB ("RGB") color mode, RGB color values can be used
        \~chinese
        清除画布并同时填充颜色
        @param fillColor: 颜色值
        @note 
            fillColor 取值范围取决于 _buffer_color_mode 的设定。
            * 如果是 SS_COLOR_MODE_MONO ("1") 单色模式，只能选择 0:黑色 和 1:白色 
            * 如果是 SS_COLOR_MODE_RGB ("RGB") 彩色模式，可以使用 RGB 色彩值
        """
        self.Canvas.rectangle((0, 0, self._display_size[0], self._display_size[1]), outline=0, fill=fillColor)
    
    def clearView(self, fillColor = 0 ):
        """!
        \~english
        Clear up canvas with view size
        @param fillColor: a color value
        @note 
            The fillColor value range depends on the setting of _buffer_color_mode.
            * If it is SS_COLOR_MODE_MONO ("1") monochrome mode, it can only select 0: black and 1: white
            * If it is SS_COLOR_MODE_RGB ("RGB") color mode, RGB color values can be used

        \~chinese
        清除画布中当前视图大小的区域同时填充颜色
        @param fillColor: 颜色值
        @note 
            fillColor 取值范围取决于 _buffer_color_mode 的设定。
            * 如果是 SS_COLOR_MODE_MONO ("1") 单色模式，只能选择 0:黑色 和 1:白色 
            * 如果是 SS_COLOR_MODE_RGB ("RGB") 彩色模式，可以使用 RGB 色彩值
        """
        self.Canvas.rectangle(self.View.rectToArray(), outline=0, fill=fillColor)

    def clear(self):
        """!
        \~english
        Clear display and screen's canvas
        \~chinese
        同时清除显示屏和画布
        """
        self.clearCanvas()
        self.Display.clear()
        pass

    def redefineBuffer(self, newBuffer ):
        """!
        \~english 
        Redefine frame of Screen
        @param newFrame: a new fram data
        @note
            newFrame can be:
            * PIL Image
            * PIL ImageFile
            * Dictionary, eg. { "size":(width, height), "color_mode":"1" } or { "size":(width, height), "color_mode":"RGB" }

        \~chinese
        重新定义缓存数据
        @param newFrame: 新缓存数据 \n
            newFrame 可以为下面值:
            * PIL Image
            * PIL ImageFile
            * 字典, eg. { "size":(width, height), "color_mode":"1" } or { "size":(width, height), "color_mode":"RGB" } 
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
            self._buffer = Image.new( newBuffer["color_mode"] , newBuffer["size"] )
            self.Canvas = ImageDraw.Draw( self._buffer )
            return True
        pass

    pass