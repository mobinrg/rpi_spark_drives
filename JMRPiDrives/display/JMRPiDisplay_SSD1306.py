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
#    JMRPi OLED display ssd1306
#    by Kunpeng Zhang
#    v1.0.0    2018.3.20
#

import RPi.GPIO as GPIO
import spidev
from PIL import Image
from .JMRPiDisplay import SSDiaplayBase

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

# This command stops the motion of scrolling. After sending 2Eh command to deactivate the scrolling action,
# the ram data needs to be rewritten.
CMD_SSD1306_SET_SCROLL_DEACTIVE     = 0x2E

# This command starts the motion of scrolling and should only be issued after the scroll setup parameters have
# been defined by the scrolling setup commands :26h/27h/29h/2Ah . The setting in the last scrolling setup
# command overwrites the setting in the previous scrolling setup commands.
CMD_SSD1306_SET_SCROLL_ACTIVE       = 0x2F

# This command consists of consecutive bytes to set up the horizontal scroll parameters and determines the
# scrolling start page, end page and scrolling speed.
CMD_SSD1306_SET_SCROLL_HORIZONTAL_RIGHT  = 0x26
CMD_SSD1306_SET_SCROLL_HORIZONTAL_LEFT = 0x27

# This command consists of 6 consecutive bytes to set up the continuous vertical scroll parameters and
# determines the scrolling start page, end page, scrolling speed and vertical scrolling offset.
# The bytes B[2:0], C[2:0] and D[2:0] of command 29h/2Ah are for the setting of the continuous horizontal
# scrolling. The byte E[5:0] is for the setting of the continuous vertical scrolling offset. All these bytes together
# are for the setting of continuous diagonal (horizontal + vertical) scrolling. If the vertical scrolling offset byte
# E[5:0] is set to zero, then only horizontal scrolling is performed (like command 26/27h).
CMD_SSD1306_SET_SCROLL_HORIZONTAL_VERTICAL_RIGHT = 0x29
CMD_SSD1306_SET_SCROLL_HORIZONTAL_VERTICAL_LEFT  = 0x2A

# This command consists of 3 consecutive bytes to set up the vertical scroll area. For the continuous vertical
# scroll function (command 29/2Ah), the number of rows that in vertical scrolling can be set smaller or equal to
# the MUX ratio.
CMD_SSD1306_SET_SCROLL_VERTICAL_AREA= 0xA3


class SSD1306Base( SSDiaplayBase ):
    #mirror horizontal
    _mirror_h = 0
    #mirror vertical
    _mirror_v = 0
    
    _mem_pages = 0

    def _command(self, commands):
        """Send command to ssd1306, DC pin need set to LOW """
        if self._spi == None: raise "Do not setting SPI"
        GPIO.output( self._spi_dc, 0 )
        self._spi.writebytes( commands )

    def _data(self, data):
        """Send data to ssd1306, DC pin need set to HIGH """
        if self._spi == None: raise "Do not setting SPI"
        GPIO.output( self._spi_dc, 1 )
        self._spi.writebytes( data )

    def _display_buffer(self, buffer ):
        """Send buffer data to physical display."""
        self._command([
            CMD_SSD1306_SET_COLUMN_ADDR,
            0, self.width-1,
            CMD_SSD1306_SET_PAGE_ADDR,
            0, self._mem_pages - 1
            ])
        self._data( buffer )

    def _init_display(self):
        self._command([
            # 0xAE
            CMD_SSD1306_DISPLAY_OFF,
            #Stop Scroll
            CMD_SSD1306_SET_SCROLL_DEACTIVE,
            # 0xA8 SET MULTIPLEX 0x3F
            CMD_SSD1306_SET_MULTIPLEX_RATIO,
            0x3F,
            # 0xD3 SET DISPLAY OFFSET
            CMD_SSD1306_SET_DISPLAY_OFFSET,
            0x00,
            # 0x40 Set Mapping RAM Display Start Line  (0x00~0x3F)
            CMD_SSD1306_SET_DISPLAY_START_LINE,
            # 0xDA Set COM Pins hardware configuration, (0x00/0x01/0x02)
            CMD_SSD1306_SET_COM_PINS,
            (0x02 | 0x10),
            CMD_SSD1306_SET_CONTRAST,
            0x7F,
            # 0xA4 Disable Entire Display On
            CMD_SSD1306_ENTIRE_DISPLAY_ON_0,
            # 0xA6 Set normal display
            CMD_SSD1306_NORMAL_DISPLAY,
            # 0xA7 Set inverse display
            # CMD_SSD1306_INVERSE_DISPLAY, 
            # 0xD5 Set osc frequency 0x80
            CMD_SSD1306_SET_CLOCK_DIVIDE_RATIO,
            0x80,
            # 0x8D Enable DC/DC charge pump regulator 0x14
            CMD_SSD1306_CHARGE_PUMP,
            0x14,
            # 0x20 Set Page Addressing Mode (0x00/0x01/0x02)
            CMD_SSD1306_SET_MEM_ADDR_MODE,
            0x01,
  
            # 0xC0 / 0xC8 Set COM Output Scan Direction
            #CMD_SSD1306_SCAN_DIRECTION_INC,
            #CMD_SSD1306_SCAN_DIRECTION_DEC,
            CMD_SSD1306_SCAN_DIRECTION_INC if self._mirror_v else CMD_SSD1306_SCAN_DIRECTION_DEC,
  
            # 0xA0 / oxA1 Set Segment re-map
            # 0xA0    left to right
            # 0xA1    right to left
            CMD_SSD1306_SET_SEGMENT_REMAP_0 if self._mirror_h else CMD_SSD1306_SET_SEGMENT_REMAP_1,
        ])

    def init(self):
        self._init_io()
        self.reset()
        self._init_display()

    def clear(self, fill = 0x00):
        self._buffer = [ fill ] * ( self.width * self._mem_pages )

    def on(self):
        self._command( [CMD_SSD1306_DISPLAY_ON] )

    def off(self):
        self._command( [CMD_SSD1306_DISPLAY_OFF] )

    def reset(self):
        """Reset display"""
        if self._spi_reset == None: return
        GPIO.output( self._spi_reset, 1 )
        time.sleep(0.002)
        GPIO.output( self._spi_reset, 0 )
        time.sleep(0.015)
        GPIO.output( self._spi_reset, 1 )

    def setContrast(self, contrast):
        self._command([CMD_SSD1306_SET_CONTRAST])
        self._command([contrast])

#         self._command([CMD_SSD1306_SET_CONTRAST, contrast])
        
    def setBrightness(self, brightness):
        raise ValueError("Has not brightness controller") 

    def display(self, buffer = None):
        """Write buffer to physical display."""
        if buffer != None:
            self._display_buffer( buffer )
        else:
            self._display_buffer( self._buffer )
            
    def setImage(self, image):
        """Convert image to the buffer, The image mode must be 1 and image size equal to the display size
         image type is Python Imaging Library image.
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
        self._command([CMD_SSD1306_SET_SCROLL_ACTIVE])
        
    def scrollOff(self):
        self._command([CMD_SSD1306_SET_SCROLL_DEACTIVE])

    def scrollWith(self, hStart = 0x00, hEnd=0x00, vOffset = 0x00, vStart=0x00, vEnd=0x00, int = 0x00, dire = "left" ):
        """Scroll screen
            hStart:  Set horizontal scroll PAGE start address, value can be chose between 0 and 7
            hEnd:  Set horizontal scroll PAGE end address, value can be chose between 0 and 7
            vOffset: Vertical scroll offset row, if set to 0x00(0) mean is off vertical scroll
            vStart: Vertical scroll start line, value can be chose between 0x00 and screen.height
            vEnd: Vertical scroll end line, value can be chose between 0x00 and screen.height
            int: Set time interval between each scroll step
            dire: Set scroll direction, value can be "left" or "right"
        """
        self._command( [CMD_SSD1306_SET_SCROLL_DEACTIVE] )
        if vOffset != 0:
            self._command( [
                    CMD_SSD1306_SET_SCROLL_VERTICAL_AREA,
                    vStart,
                    vEnd,
                    0x00
                ])

        self._command( [
            CMD_SSD1306_SET_SCROLL_HORIZONTAL_VERTICAL_LEFT if dire.upper()=="LEFT" else CMD_SSD1306_SET_SCROLL_HORIZONTAL_VERTICAL_RIGHT,
            0x00, 
            hStart, 
            int, 
            hEnd, 
            vOffset, 
            0x00,
            CMD_SSD1306_SET_SCROLL_ACTIVE
            ])


class SSD1306_128x64(SSD1306Base):
    def __init__( self, spi=None, spiMosi= None, spiDC=None, spiCS=None, spiReset=None, spiClk=None, mirrorH = 0, mirrorV = 0  ):        
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
