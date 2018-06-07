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
#    Base Display
#    by Kunpeng Zhang
#    v1.0.0    2018.3.20
#

import RPi.GPIO as GPIO
import spidev

class SSDiaplayBase:
    width = 0
    height = 0

    # SPI interface
    _spi        = None
    _spi_mosi   = None
    _spi_dc     = None
    _spi_cs     = None
    _spi_reset  = None
    _spi_clk    = None

    # display buffer
    _buffer = []

    def _command(self, commands):
#         """Send command to spi bus of display chip, most DC pin need set to LOW """
#         if self._spi == None: raise "Do not setting SPI"
#         GPIO.output( self._spi_dc, 0 )
#         self._spi.writebytes( commands )
        raise NotImplementedError

    def _data(self, data):
#         """Send data to spi bus of display chip, most DC pin need set to HIGH """
#         if self._spi == None: raise "Do not setting SPI"
#         GPIO.output( self._spi_dc, 1 )
#         self._spi.writebytes( data )
        raise NotImplementedError

    def _init_config(self, width, height, spi=None, spiMosi= None, spiDC=None, spiCS=None, spiReset=None, spiClk=None):
        self._spi = spi
        self._spi_mosi = spiMosi
        self._spi_dc = spiDC
        self._spi_cs = spiCS
        self._spi_reset = spiReset
        self._spi_clk = spiClk
        
        self.width = width
        self.height = height
        
    def _init_io(self):
        GPIO.setwarnings(False)
        GPIO.setmode( GPIO.BCM )
        pins = [ self._spi_dc ]
        for pin in pins:
            GPIO.setup( pin, GPIO.OUT )

    def _init_display(self):
        raise NotImplementedError

    def __init__ ( self, width, height, spi=None, spiMosi= None, spiDC=None, spiCS=None, spiReset=None, spiClk=None ):
        self._init_config(width, height, spi, spiMosi, spiDC, spiCS, spiReset, spiClk)

    def clear(self, fill = 0x00):
        self._buffer = [ fill ] * ( self.width * self.height )

    def on(self):
        raise NotImplementedError

    def off(self):
        raise NotImplementedError

    def init(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError
    
    def setContrast(self, contrast):
        raise NotImplementedError
    
    def setBrightness(self, brightness):
        raise NotImplementedError
    
    def display(self, buffer = None):
        raise NotImplementedError
    
    def setImage(self, image):
        raise NotImplementedError
        