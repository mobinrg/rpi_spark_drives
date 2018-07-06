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
#    RPi OLED display ssd1306
#    @author Kunpeng Zhang
#    v1.0.0    2018.3.20
#

import RPi.GPIO as GPIO
import spidev
from PIL import Image
from .RPiDisplay import RPiDiaplay

class SSD1306Base( RPiDiaplay ):
    """!
    \~english SSD1306 Display Chip
    \~chinese SSD1306 显示芯片驱动
    """
    CMD_SSD1306_SET_MEM_ADDR_MODE       = 0x20
    CMD_SSD1306_SET_COLUMN_ADDR         = 0x21
    CMD_SSD1306_SET_PAGE_ADDR           = 0x22
    CMD_SSD1306_SET_DISPLAY_START_LINE  = 0x40  # 0x40(0) ~ 0x7F(63)
    CMD_SSD1306_SET_CONTRAST            = 0x81  # 0x00~0xFF
    CMD_SSD1306_SET_SEGMENT_REMAP_0     = 0xA0
    CMD_SSD1306_SET_SEGMENT_REMAP_1     = 0xA1
    CMD_SSD1306_ENTIRE_DISPLAY_ON_0     = 0xA4
    CMD_SSD1306_ENTIRE_DISPLAY_ON_1     = 0xA5
    CMD_SSD1306_NORMAL_DISPLAY          = 0xA6
    CMD_SSD1306_INVERSE_DISPLAY         = 0xA7
    CMD_SSD1306_SET_MULTIPLEX_RATIO     = 0xA8
    CMD_SSD1306_DISPLAY_OFF             = 0xAE
    CMD_SSD1306_DISPLAY_ON              = 0xAF
    CMD_SSD1306_CHARGE_PUMP             = 0x8D
    # CMD_SSD1306_SET_START_ADDR_PAGE_ADDR_MODE
    CMD_SSD1306_SCAN_DIRECTION_INC      = 0xC0
    CMD_SSD1306_SCAN_DIRECTION_DEC      = 0xC8
    CMD_SSD1306_SET_DISPLAY_OFFSET      = 0xD3
    CMD_SSD1306_SET_CLOCK_DIVIDE_RATIO  = 0xD5
    CMD_SSD1306_SET_PRECHARGE           = 0xD9
    CMD_SSD1306_SET_COM_PINS            = 0xDA
    CMD_SSD1306_SET_DESELECT_LEVEL      = 0xDB
    
    #Graphic Acceleration Command
    
    # This command stops the motion of scrolling. After sending 2Eh command to 
    # deactivate the scrolling action, the ram data needs to be rewritten. 
    CMD_SSD1306_SET_SCROLL_DEACTIVE     = 0x2E
    
    # This command starts the motion of scrolling and should only be issued after 
    # the scroll setup parameters have been defined by the scrolling setup 
    # commands:26h/27h/29h/2Ah . The setting in the last scrolling setup
    # command overwrites the setting in the previous scrolling setup commands.
    CMD_SSD1306_SET_SCROLL_ACTIVE       = 0x2F
    
    # This command consists of consecutive bytes to set up the horizontal scroll 
    # parameters and determines the scrolling start page, end page and scrolling
    # speed.
    CMD_SSD1306_SET_SCROLL_HORIZONTAL_RIGHT  = 0x26
    CMD_SSD1306_SET_SCROLL_HORIZONTAL_LEFT = 0x27
    
    # This command consists of 6 consecutive bytes to set up the continuous 
    # vertical scroll parameters and determines the scrolling start page, end 
    # page, scrolling speed and vertical scrolling offset. 
    # The bytes B[2:0], C[2:0] and D[2:0] of command 29h/2Ah are for the setting 
    # of the continuous horizontal scrolling. The byte E[5:0] is for the setting 
    # of the continuous vertical scrolling offset. All these bytes together are 
    # for the setting of continuous diagonal (horizontal + vertical) scrolling. 
    # If the vertical scrolling offset byte E[5:0] is set to zero, then only 
    # horizontal scrolling is performed (like command 26/27h).
    CMD_SSD1306_SET_SCROLL_HORIZONTAL_VERTICAL_RIGHT = 0x29
    CMD_SSD1306_SET_SCROLL_HORIZONTAL_VERTICAL_LEFT  = 0x2A
    
    # This command consists of 3 consecutive bytes to set up the vertical scroll 
    # area. For the continuous vertical
    # scroll function (command 29/2Ah), the number of rows that in vertical 
    # scrolling can be set smaller or equal to the MUX ratio.
    CMD_SSD1306_SET_SCROLL_VERTICAL_AREA= 0xA3
    
    ## 
    # \~english mirror horizontal (boolean)
    # \~chinese 水平镜像 (boolean)
    _mirror_h = None
    ## 
    # \~english mirror vertical (boolean)
    # \~chinese 垂直镜像 (boolean)
    _mirror_v = None
    ## 
    # \~english buffer page (int)
    # \~chinese 显存分页 (int)
    _mem_pages = None

    def _command(self, commands):
        """!
        \~english
        Send command to ssd1306, DC pin need set to LOW
        @param commands: an byte or array of bytes

        \~chinese 
        发送命令给 SSD1306，DC 需要设定为低电平 LOW
        @param commands: 一个字节或字节数组
        """
        if self._spi == None: raise "Do not setting SPI"
        GPIO.output( self._spi_dc, 0 )
        self._spi.writebytes( commands )

    def _data(self, data):
        """!
        \~english
        Send data to ssd1306, DC pin need set to HIGH
        @param data: sent to display chip of data. it can be an byte or array of bytes

        \~chinese
        发送数据给 SSD1306, DC 需要设定为高电平 HIGH
        @param data: 送到显示芯片的数据。 可以是一个字节或字节数组
        """
        if self._spi == None: raise "Do not setting SPI"
        GPIO.output( self._spi_dc, 1 )
        self._spi.writebytes( data )

    def _display_buffer(self, buffer ):
        """!
        \~english
        Send buffer data to physical display.
        @param buffer: sent to display chip of data.

        \~chinese
        将缓冲区数据发送到物理显示。
        @param buffer: 送到显示芯片的数据。
        """
        self._command([
            self.CMD_SSD1306_SET_COLUMN_ADDR,
            0, self.width-1,
            self.CMD_SSD1306_SET_PAGE_ADDR,
            0, self._mem_pages - 1
            ])
        self._data( buffer )

    def _init_display(self):
        """!
        \~english
        Initialize the SSD1306 display chip

        \~chinese
        初始化SSD1306显示芯片
        """
        self._command([
            # 0xAE
            self.CMD_SSD1306_DISPLAY_OFF,
            #Stop Scroll
            self.CMD_SSD1306_SET_SCROLL_DEACTIVE,
            # 0xA8 SET MULTIPLEX 0x3F
            self.CMD_SSD1306_SET_MULTIPLEX_RATIO,
            0x3F,
            # 0xD3 SET DISPLAY OFFSET
            self.CMD_SSD1306_SET_DISPLAY_OFFSET,
            0x00,
            # 0x40 Set Mapping RAM Display Start Line  (0x00~0x3F)
            self.CMD_SSD1306_SET_DISPLAY_START_LINE,
            # 0xDA Set COM Pins hardware configuration, (0x00/0x01/0x02)
            self.CMD_SSD1306_SET_COM_PINS,
            (0x02 | 0x10),
            self.CMD_SSD1306_SET_CONTRAST,
            0x7F,
            # 0xA4 Disable Entire Display On
            self.CMD_SSD1306_ENTIRE_DISPLAY_ON_0,
            # 0xA6 Set normal display
            self.CMD_SSD1306_NORMAL_DISPLAY,
            # 0xA7 Set inverse display
            # CMD_SSD1306_INVERSE_DISPLAY, 
            # 0xD5 Set osc frequency 0x80
            self.CMD_SSD1306_SET_CLOCK_DIVIDE_RATIO,
            0x80,
            # 0x8D Enable DC/DC charge pump regulator 0x14
            self.CMD_SSD1306_CHARGE_PUMP,
            0x14,
            # 0x20 Set Page Addressing Mode (0x00/0x01/0x02)
            self.CMD_SSD1306_SET_MEM_ADDR_MODE,
            0x01,
  
            # 0xC0 / 0xC8 Set COM Output Scan Direction
            #CMD_SSD1306_SCAN_DIRECTION_INC,
            #CMD_SSD1306_SCAN_DIRECTION_DEC,
            self.CMD_SSD1306_SCAN_DIRECTION_INC if self._mirror_v else self.CMD_SSD1306_SCAN_DIRECTION_DEC,
  
            # 0xA0 / oxA1 Set Segment re-map
            # 0xA0    left to right
            # 0xA1    right to left
            self.CMD_SSD1306_SET_SEGMENT_REMAP_0 if self._mirror_h else self.CMD_SSD1306_SET_SEGMENT_REMAP_1,
        ])

    def init(self):
        """!
        \~english
        Initialize the SSD1306 display chip, and ready for show something
        \~chinese
        初始化SSD1306显示芯片，并准备好接收显示命令和数据
        """
        self._init_io()
        self.reset()
        self._init_display()

    def clear(self, fill = 0x00):
        """!
        \~english
        Clear buffer data and fill color into buffer
        @param fill: a color value, it will fill into buffer.<br>
                The SSD1306 only chosen two colors: <br>
                   0 (0x0): black <br>
                   1 (0x1): white <br>

        \~chinese
        清除缓冲区数据并在缓冲区中填充颜色
        @param fill: 一个颜色值，它会填充到缓冲区中 <br>
                     SSD1306只能选择两种颜色： <br>
                        0（0x0）：黑色 <br>
                        1（0x1）：白色 <br>
        """
        self._buffer = [ fill ] * ( self.width * self._mem_pages )

    def on(self):
        """!
        \~english power on display.
        \~chinese 开启显示屏
        """
        self._command( [self.CMD_SSD1306_DISPLAY_ON] )

    def off(self):
        """!
        \~english power off display.
        \~chinese 关闭显示屏
        """
        self._command( [self.CMD_SSD1306_DISPLAY_OFF] )

    def reset(self):
        """!
        \~english Reset display
        \~chinese 复位显示屏
        """
        if self._spi_reset == None: return
        GPIO.output( self._spi_reset, 1 )
        time.sleep(0.002)
        GPIO.output( self._spi_reset, 0 )
        time.sleep(0.015)
        GPIO.output( self._spi_reset, 1 )

    def setContrast(self, contrast):
        """!
        \~english 
        Change contrast of SSD1306 display chip
        @param contrast: a contrast value, the range is: 0-255
        
        \~chinese 
        改变 SSD1306 显示屏对比度
        @param contrast: 对比度值，范围是：0-255
        """
        self._command([self.CMD_SSD1306_SET_CONTRAST, contrast])
        
    def setBrightness(self, brightness):
        """!
        \~english 
        @deprecated SSD1306 do not supported brightness justment
        \~chinese 
        @deprecated SSD1306不支持亮度调整
        """
        raise ValueError("Has not brightness controller")

    def display(self, buffer = None):
        """!
        \~english 
        Write buffer to physical display.
        @param buffer: Data to display，If <b>None</b> mean will use self._buffer data to display
        \~chinese 
        将缓冲区写入物理显示屏。
        @param buffer: 要显示的数据，如果是 <b>None</b>(默认) 将把 self._buffer 数据写入物理显示屏 
        """
        if buffer != None:
            self._display_buffer( buffer )
        else:
            self._display_buffer( self._buffer )
            
    def setImage(self, image):
        """!
        \~english
        Convert image to the buffer, The image mode must be 1 and image size 
        equal to the display size image type is Python Imaging Library image.
        @param image: a PIL image object

        \~chinese
        将图像转换为缓冲区，这个图像的色彩模式必须为 1 同时图像大小必须等于显存大小，
        图像类型： PIL Image (Python Imaging Library)
        @param image: PIL图像对象

        \n \~
        @note
        <pre>
        ssd1306.setImage( aPILImage )
        ssd1306.display()
        </pre>
        """
        if image.mode != '1':
            raise ValueError('The image color must be in mode \"1\".')

        imgWidth, imgHeight = image.size
        if imgWidth != self.width or imgHeight != self.height:
            raise ValueError('The image must be same dimensions as display ( {0} x {1} ).' \
                .format(self.width, self.height))

        # First then shift left 
        pixByte = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
        bi = 0
        pixs = image.load()
        for x in range( 0, self.width ):
            for y in range( 0, self.height, 8 ):
                pixBits = 0x00
                # first then range(8)
                for py in [0,1,2,3,4,5,6,7]:
                    pixBits |= (0x00 if pixs[x, y+py] == 0 else pixByte[py])
                self._buffer[bi] = pixBits
                bi += 1

    def scrollOn(self):
        """!
        \~english 
        Start scroll screen
        use: SSD1306Base#scrollWith to set up scroll mode
        \~chinese 
        开始滚屏
        使用：SSD1306Base#scrollWith 设置滚动模式
        """
        self._command([self.CMD_SSD1306_SET_SCROLL_ACTIVE])
        
    def scrollOff(self):
        """!
        \~english Stop scroll screen
        \~chinese 停止滚屏
        
        \n \~
        @see scrollOn
        """
        self._command([self.CMD_SSD1306_SET_SCROLL_DEACTIVE])

    def scrollWith(self, hStart = 0x00, hEnd=0x00, vOffset = 0x00, vStart=0x00, vEnd=0x00, int = 0x00, dire = "left" ):
        """!
        \~english 
        Scroll screen
        @param hStart: Set horizontal scroll PAGE start address, value can be chosen between 0 and 7
        @param hEnd:  Set horizontal scroll PAGE end address, value can be chose between 0 and 7
        @param vOffset: Vertical scroll offset row, if set to 0x00(0) means off vertical scroll
        @param vStart: Vertical scroll start line, value can be chose between 0x00 and screen.height
        @param vEnd: Vertical scroll end line, value can be chose between 0x00 and screen.height
        @param int: Set time interval between each scroll step
        @param dire: Set scroll direction, value can be "left" or "right"
        
        \~chinese
        屏幕滚动
        @param hStart: 设置水平滚动PAGE起始地址，数值可以在0到7之间选择
        @param hEnd:  设置水平滚动PAGE结束地址，值可以在0和7之间选择
        @param vOffset: 垂直滚动偏移行，如果设置为0x00（0），表示关闭垂直滚动
        @param vStart: 垂直滚动起始行，值可以在0x00和screen.height之间选择
        @param vEnd: 垂直滚动结束行，值可以在0x00和screen.height之间选择
        @param int: 设置每个滚动步骤之间的时间间隔
        @param dire: 设置滚动方向，数值可以是 "left" 或 "right"
        """
        self._command( [self.CMD_SSD1306_SET_SCROLL_DEACTIVE] )
        if vOffset != 0:
            self._command( [
                    self.CMD_SSD1306_SET_SCROLL_VERTICAL_AREA,
                    vStart,
                    vEnd,
                    0x00
                ])

        self._command( [
            self.CMD_SSD1306_SET_SCROLL_HORIZONTAL_VERTICAL_LEFT if dire.upper()=="LEFT" else self.CMD_SSD1306_SET_SCROLL_HORIZONTAL_VERTICAL_RIGHT,
            0x00, 
            hStart, 
            int, 
            hEnd, 
            vOffset, 
            0x00,
            self.CMD_SSD1306_SET_SCROLL_ACTIVE
            ])


class SSD1306_128x64(SSD1306Base):
    """!
    \~english 
    128x64 OLED of SSD1306 Display Chip
    uses: SPI

    \~chinese
    SSD1306 128x64 OLED 显示芯片驱动, 使用 SPI 总线
    """
    def __init__( self, spi=None, spiMosi= None, spiDC=None, spiCS=None, spiReset=None, spiClk=None, mirrorH = 0, mirrorV = 0  ):
        """!
        \~english Initialize the SSD1306 128x64 OLED display object instance and config GPIO and others
        \~chinese 实例化 SSD1306 128x64 OLED 显示屏对象，同时初始化 GPIO 和其他

        \~english
        @param spi: a spi bus object instance
        @param spiMosi: spi mosi io number, eg. 10 default is None
        @param spiDC: spi dc io number, eg. 9 default is None
        @param spiCS: spi cs io number, eg. 8 default is None
        @param spiReset: spi reset io number, eg. 18 default is None. <br>
                        If <b>None</b> mean this chip do not need reset
        @param spiClk: spi clk io number, eg. 11 default is None
        @param mirrorH: The displayed image flips horizontal
        @param mirrorV: The displayed image flips vertically
        
        \~chinese
        @param spi: SPI 总线对象实例
        @param spiMosi: SPI MOSI IO, 例如： 10, 默认: None
        @param spiDC: SPI DC IO, 例如： 9, 默认: None
        @param spiCS: SPI CS IO, 例如： 8, 默认: None
        @param spiReset: SPI RESET IO, 例如： 18, 默认: None <br>
                        如果是 <b>None</b> 停用 SPI RESET 功能
        @param spiClk: SPI CLK IO, 例如：11， 默认 None
        @param mirrorH: 显示屏水平镜向显示
        @param mirrorV: 显示屏垂直镜向显示

        \~
        @note
        \~english A siample for use SSD1306_128x64 below:
        \~chinese 使用 SSD1306_128x64 示例：
        \~\n
        <hr>
        <pre>
        import spidev
        from PIL import Image
        from JMRPiSpark.Drives.Display.SSD1306 import SSD1306_128x64 \n
        class CONFIG_DSP:
            DSP_RESET       = None
            DSP_DC          = 9
            DSP_SPI_PORT    = 0
            DSP_SPI_DEVICE  = 0
            DSP_SPI_MAX_SPEED_HZ = 2000000
            DSP_MIRROR_H    = True
            DSP_MIRROR_V    = True \n
        spi = spidev.SpiDev()
        spi.open( CONFIG_DSP.DSP_SPI_PORT, CONFIG_DSP.DSP_SPI_DEVICE)
        spi.max_speed_hz = CONFIG_DSP.DSP_SPI_MAX_SPEED_HZ
        spi.cshigh = False
        spi.mode = 0 \n
        myDSP = SSD1306_128x64 ( 
            spi,  
            spiDC = CONFIG_DSP.DSP_DC,
            spiReset = CONFIG_DSP.DSP_RESET,
            mirrorH = CONFIG_DSP.DSP_MIRROR_H, 
            mirrorV = CONFIG_DSP.DSP_MIRROR_V
            ) \n
        myDSP.init()
        myDSP.on()
        </pre>
        """
        self._init_config(128, 64, spi, spiMosi, spiDC, spiCS, spiReset, spiClk)
        self._mirror_h = mirrorH
        self._mirror_v = mirrorV
        self._mem_pages = 64 //8
        self._buffer = [0] * ( 128 * self._mem_pages )

# class SSD1306_128x32(SSD1306Base):
#     def __init__( self, spi=None, spiMosi= None, spiDC=None, spiCS=None, spiReset=None, spiClk=None, mirrorH = 0, mirrorV = 0  ):        
#         self._init_config(128, 32, spi, spiMosi, spiDC, spiCS, spiReset, spiClk)
#         self._mirror_h = mirrorH
#         self._mirror_v = mirrorV
#         self._mem_pages = 32 //8
#         self._buffer = [0] * ( 128 * self._mem_pages )
# 
# class SSD1306_64x32(SSD1306Base):
#     def __init__( self, spi=None, spiMosi= None, spiDC=None, spiCS=None, spiReset=None, spiClk=None, mirrorH = 0, mirrorV = 0  ):        
#         self._init_config(64, 32, spi, spiMosi, spiDC, spiCS, spiReset, spiClk)
#         self._mirror_h = mirrorH
#         self._mirror_v = mirrorV
#         self._mem_pages = 32 //8
#         self._buffer = [0] * ( 64 * self._mem_pages )
