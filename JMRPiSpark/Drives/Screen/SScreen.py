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
#    RPi-Spark ScreenBase
#    by Kunpeng Zhang
#    v1.0.0
#

# Display color mode

## Mono color mode
SS_COLOR_MODE_MONO  = "1"
## RGB color mode
SS_COLOR_MODE_RGB   = "RGB"

class SSPoint:
    """!
    \~english A point object
    \~chinese 点对象
    """
    x = 0
    y = 0

class SSRect:
    """!
    \~english A rectangles object
    \~chinese 矩形对象
    """
    x       = 0
    y       = 0
    height  = 0
    width   = 0

    def __init__(self, x, y, width, height):
        """!
        \~english Initialize the rectangles object instance
        \~chinese 初始化矩形实例
        """
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def resize(self, newWidth = 0, newHeight = 0):
        """!
        \~english 
        Resize width and height of rectangles
        @param newWidth: new width value
        @param newHeight: new height value
        \~chinese 
        重新设定矩形高宽
        @param newWidth: 新宽度
        @param newHeight: 新高度
        """
        self.height = newHeight
        self.width = newWidth

    def adjuestSize(self, offsetWidth = 0, offsetHeight = 0):
        """!
        \~english 
        Adjuest width and height of rectangles
        @param offsetWidth: adjust the width. Negative numbers are smaller, Positive number is increased
        @param offsetHeight: adjust the height. Negative numbers are smaller, Positive number is increased
        
        @note The negative numbers are smaller, positive number is increased，0 remains unchanged.
        
        \~chinese
        调整矩形高宽数据
        @param offsetWidth: 调整宽度。 负数较小，正数增加
        @param offsetHeight: 调整高度。 负数较小，正数增加

        @note 负数较小，正数增加，0保持不变。
        """
        self.height += offsetHeight
        self.width += offsetWidth

    def moveTo(self, newX=0, newY=0):
        """!
        \~english 
        Move vertex of rectangles to new point (x,y)
        @param newX: Coordinated X value
        @param newY: Coordinated Y value
        \~chinese
        移动矩形到新坐标点 (x,y)
        @param newX: 坐标 X
        @param newY: 坐标 Y
        """
        self.x = newX
        self.y = newY

    def moveOffset(self, offsetX=0, offsetY=0):
        """!
        \~english 
        Offset vertex of rectangles to new point (x,y)
        @param offsetX: offset X value
        @param offsetY: offset Y value
        @note The negative numbers are left or up move , positive number is right or down move，0 remains unchanged.
        \~chinese
        平移矩形指定的距离 (x,y)
        @param offsetX: 平移 X
        @param offsetY: 平移 Y
        @note 负数是左移( X )或上移( Y )，正数是右移( X )或下移( Y )，0 保持不变。
        """
        self.x += offsetX
        self.y += offsetY

    def swapWH(self):
        """!
        \~english Swap width and height of rectangles
        \~chinese 交换矩形高宽边数据
        """
        width = self.width
        self.width = self.height
        self.height = width

    def rectToArray(self, swapWH = False):
        """!
        \~english
        Rectangles converted to array of coordinates
        @return: an array of rect points. eg. (x1,y1,x2,y2)

        \~chinese
        矩形数据转换为矩形坐标数组
        @return: 矩形座标数组, 例如: ( x1,y1,x2,y2 )
        """
        if swapWH == False:
            return [self.x, self.y, self.x + self.width, self.y + self.height]
        else:
            return [self.x, self.y, self.x + self.height, self.y + self.width]

class SScreenBase:
    """!
    \~english
    SScreenBase is a hardware abstraction of the screen，
    it contain a Display, a Canvas and a View instances
    You need to create a subclass from inherit it and 
    use the new subclass implement initialization and 
    operations of screen.

    \~chinese
    SScreenBase是屏幕的硬件抽象，它包含一个 Display，一个 Canvas 和一个 View 实例
    你需要通过继承和创建一个子类, 使用新的子类实现初始化和屏幕的操作。
    """
    ##
    # \~english a display hardware instance
    # \~chinese 显示屏芯片硬件实例
    Display = None
    ##
    # \~english a canvas instance. you can draw something on it, then call SScreenBase#refresh to update to display
    # \~chinese 画布实例，可以绘制图像文字，然后通过 SScreenBase#refresh 更新到显示屏
    Canvas = None
    ##
    # \~english a SSRect instance. 
    # \~chinese SSRect 实例.
    View = None

    # Display direction can choos in 0, 90, 180, 270
    _display_direction = None
    # Display's size, it init at intance when __init__ (x,y), and it keep same direction whit "_display_direction"
    # If you need to access the physical size, use the “Display” object
    _display_size = None #(0,0)
    
    ##
    # display color mode, it is readonly, can not be change. 
    # it can be chosen: SS_COLOR_MODE_MONO ("1"): greyscale or SS_COLOR_MODE_RGB ("RGB"): image
    _display_color_mode = None #SS_COLOR_MODE_MONO
    
    ##
    # buffer color mode, it is can be change using SScreenBase#changeBufferColorMode,
    # and it can diffent from _display_color_mode,
    # its value could be: SS_COLOR_MODE_MONO ("1"): greyscale or SS_COLOR_MODE_RGB ("RGB"): color
    _buffer_color_mode = None #SS_COLOR_MODE_MONO

    ##
    # Screen buffer, its size can diffent from display size.
    _buffer = None

    def __init__(self, display, bufferColorMode, bufferSize=None, displayDirection=0 ):
        raise NotImplementedError

    def _initDisplay(self, display, displayDirection, displaySize=(0,0)):
        self._display_direction = displayDirection

        if self._needSwapWH(0, displayDirection):
            self._display_size = ( displaySize[1], displaySize[0] )
        else:
            self._display_size = displaySize

        self.Display = display

    def _initBuffer(self, bufferColorMode, bufferSize):
        self._buffer_color_mode = bufferColorMode

    def _needSwapWH(self, oldDirection, newDirection ):
        """!
        \~english
        return screen direction status
        @return Boolean
        @note No need to rotate if the screen orientation is 0 degrees and 180 degrees

        \~chinese
        返回屏幕方向状态
        @return 布尔值
        @note 如果屏幕方向是0度和180度就不需要旋转
        """
        if abs(newDirection - oldDirection) == 0: return False
        if abs(newDirection - oldDirection) % 180 == 0: return False
        if abs(newDirection - oldDirection) % 90 == 0: return True
        return False

    def _checkBufferColorMode(self, bufferColorMode):
        """!
        \~english
        Check buffer color mode
        @param bufferColorMode: 

        \~chinese
        检测缓存色彩模式
        @param bufferColorMode: 
        """
        if bufferColorMode != SS_COLOR_MODE_RGB and bufferColorMode != SS_COLOR_MODE_MONO:
            raise ValueError("Incorrect bufferColorMode mode, this value just can be chosen: \"RGB\" or \"1\" ")

    def refresh(self):
        """!
        \~english Update current view content to display
        \~chinese 更新当前 View 内容到显示屏
        """
        raise NotImplementedError

    def clear(self):
        """!
        \~english Clear screen
        \~chinese 清屏
        """
        raise NotImplementedError

    def rotateDirection(self, displayDirection):
        """!
        \~english rotate screen direction
        @param displayDirection: Screen Direction. value can be chosen: 0, 90, 180, 270
        \~chinese 旋转显示屏方向
        @param displayDirection: 显示屏方向。可选值： 0, 90, 180, 270
        
        \~
        @note
        \~english after rotate the View resize to screen size 
        \~chinese 改变方向后，默认的 View 大小会更新为当前 Screen 的大小
        \~\n
        """
        if self._needSwapWH(self._display_direction, displayDirection):
            self._display_size = ( self._display_size[1], self._display_size[0] )
            if self.redefineBuffer( { "size":self._display_size, "color_mode":self._buffer_color_mode } ):
                self.View.resize(self._display_size[0], self._display_size[1])
        self._display_direction = displayDirection

    def redefineBuffer(self, newFrame ):
        """!
        \~english 
        Redefine frame of Screen
        @param newFrame: an Image or a Dictionary { "size", "color_mode", etc. }
        \~chinese 
        重新定义缓存数据
        @param newFrame: 图像 或 缓存字典 { "size", "color_mode", etc. }
        """
        raise NotImplementedError

    def changeBufferColorMode(self, newColorMode = SS_COLOR_MODE_MONO):
        """!
        \~english 
        Change buffer color mode
        @param newColorMode: new color mode. it can be chosen: { SS_COLOR_MODE_MONO | SS_COLOR_MODE_RGB }
        \~chinese
        改变缓存色彩模式
        @param newColorMode: 新色彩模式。 可选值： SS_COLOR_MODE_MONO 或 SS_COLOR_MODE_RGB

        \~ \n 
        @see SS_COLOR_MODE_MONO
        @see SS_COLOR_MODE_RGB
        """
        self._initBuffer(newColorMode, None)

    def getDisplaySize(self):
        return (0,0) if self._display_size==None else self._display_size

    def getBufferSize(self):
        raise NotImplementedError