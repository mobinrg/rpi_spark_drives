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
# MPU6050
#
# Author: Kunpeng Zhang
# v1.0.0    2018.04.01
#

import smbus

DEF_MPU6050_ADDRESS = 0x68

# Earth Gravitiy
GRAVITIY_EARTH  = 9.80665

class mpu6050:
    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    REG_PWR_MGMT_1 = 0x6B
    REG_PWR_MGMT_2 = 0x6C
    
    REG_ACCEL_XOUT_H = 0x3B
    REG_ACCEL_YOUT_H = 0x3D
    REG_ACCEL_ZOUT_H = 0x3F

    REG_TEMP_OUT_H = 0x41

    REG_GYRO_XOUT_H = 0x43
    REG_GYRO_YOUT_H = 0x45
    REG_GYRO_ZOUT_H = 0x47

    REG_GYRO_CONFIG     = 0x1B
    REG_ACCEL_CONFIG    = 0x1C

    #Interrupt Register
    REG_INT_PIN_CFG = 0x37      #中断/旁路设置寄存器
    REG_INT_ENABLE  = 0x38      #中断使能寄存器
    REG_INT_STATUS  = 0x3A      #中断状态寄存器

    REG_SIGNAL_PATH_RESET       = 0x68

    #Motion detect registers
    REG_MOTION_DET              = 0x1F     #运动检测阀值设置寄存器
    REG_MOTION_DET_CTRL         = 0x69     #运动检测控制寄存器
    REG_MOTION_DET_DUR          = 0x20

    #INT PIN CFG Values
    #Register 55 – INT Pin / Bypass Enable Configuration INT_PIN_CFG. page 26
    VAL_INT_PIN_CFG_INT_LEVEL       = 0x80
    VAL_INT_PIN_CFG_INT_OPEN        = 0x40
    VAL_INT_PIN_CFG_LATCH_INT_EN    = 0x20
    VAL_INT_PIN_CFG_INT_RD_CLEAR    = 0x10
    VAL_INT_PIN_CFG_FSYNC_INT_LEVEL = 0x08
    VAL_INT_PIN_CFG_FSYNC_INT_EN    = 0x04
    VAL_INT_PIN_CFG_I2C_BYPASS_EN   = 0x02

    #PWR_MGMT_1 Values
    #Register 107(0x6B) – Power Management 1 / PWR_MGMT_1. page 40
    VAL_PWR_MGMT_1_RESET    = 0x80
    VAL_PWR_MGMT_1_SLEEP    = 0x40
    VAL_PWR_MGMT_1_ON_ALL   = 0x00
    VAL_PWR_MGMT_1_ON_CYCLE = 0x20
    VAL_PWR_MGMT_1_OFF_TEMP = 0x08

    VAL_PWR_MGMT_1_CLKSEL_INTERNAL  = 0x00
    VAL_PWR_MGMT_1_CLKSEL_PLL_XG    = 0x01  #PLL with X axis gyroscope reference
    VAL_PWR_MGMT_1_CLKSEL_PLL_YG    = 0x02  #PLL with Y axis gyroscope reference
    VAL_PWR_MGMT_1_CLKSEL_PLL_ZG    = 0x03  #PLL with Z axis gyroscope reference
    VAL_PWR_MGMT_1_CLKSEL_PLL_EXT_32HZ  = 0x04  #PLL with external 32.768kHz reference
    VAL_PWR_MGMT_1_CLKSEL_PLL_EXT_19HZ  = 0x05  #PLL with external 19.2MHz reference
    VAL_PWR_MGMT_1_CLKSEL_STOP_CLK      = 0x07  #Stops the clock and keeps the timing generator in reset

    #PWR_MGMT_2 Values
    VAL_PWR_MGMT_2_LP_WAKE_CTRL_1_25HZ  = 0x00
    VAL_PWR_MGMT_2_LP_WAKE_CTRL_5HZ     = 0x40
    VAL_PWR_MGMT_2_LP_WAKE_CTRL_20HZ    = 0x80
    VAL_PWR_MGMT_2_LP_WAKE_CTRL_40HZ    = 0xC0
    
    VAL_PWR_MGMT_2_STBY_XA = 0x20
    VAL_PWR_MGMT_2_STBY_YA = 0x10
    VAL_PWR_MGMT_2_STBY_ZA = 0x08
    
    VAL_PWR_MGMT_2_STBY_XG = 0x04
    VAL_PWR_MGMT_2_STBY_YG = 0x02
    VAL_PWR_MGMT_2_STBY_ZG = 0x01
    
    #INT enable values
    VAL_INT_ENABLE_DISABLED = 0x00      #Disabled INT
    VAL_INT_ENABLE_MOTION   = 0x40      #Motion detection
    VAL_INT_ENABLE_DATA_RDY = 0x01      #Data Ready ( Gyro data do not have data in cycle mode )

    _address = None
    _bus = None
    _gravityFactor = 0;

    def __init__(self, address, busId = 1, gravityFactor = GRAVITIY_EARTH ):
        self._address = address
        self._bus = smbus.SMBus( busId )
        self._gravityFactor = gravityFactor
        self.setAccelRange( self.ACCEL_RANGE_2G )

    def readByte(self, regAddr):
        return self._bus.read_byte_data(self._address, regAddr)

    def readWord(self, regAddr):
        high = self.readByte(regAddr)
        low = self.readByte(regAddr+1)
        rawVal = ( high << 8 ) | low;
        if (rawVal >= 0x8000):
            return -((65535 - rawVal) + 1)
        else:
            return rawVal

    def writeByte(self, regAddr, regValue):
        self._bus.write_byte_data(self._address, regAddr, regValue)

    def sendCmd(self, cmd, value, firstClear = True):
        if firstClear:
            self.writeByte(cmd, 0x00)
        self.writeByte(cmd, value)

    def reset(self):
        """Reset MPU all registers
        """
        self.writeByte(self.REG_PWR_MGMT_1, self.VAL_PWR_MGMT_1_RESET)

    def open(self):
        """Trun on device and with all sensors at same time
        """
        self.sendCmd(self.REG_PWR_MGMT_1, 0x00)
        self.sendCmd(self.REG_PWR_MGMT_2, 0x00)

    def openWith(self, accel = True, gyro = True, temp = True, cycle = False, cycleFreq = 0x00):
        """Trun on device and configurable sensor and wake up mode at same time
        accel: True - enable accelerometer, 
        gyro : True - enable gyroscope, 
        temp: True - enable Thermometer, 
        cycle : True - cycle wake-up mode, 
        cycleFreq : cycle wake-up frequency, this value can be choise: 
            VAL_PWR_MGMT_2_LP_WAKE_CTRL_1_25HZ is default
            VAL_PWR_MGMT_2_LP_WAKE_CTRL_5HZ
            VAL_PWR_MGMT_2_LP_WAKE_CTRL_20HZ
            VAL_PWR_MGMT_2_LP_WAKE_CTRL_40HZ
        """
        val_pwr_2 = 0x00
        #disable Accel sensor
        if accel == False:
            val_pwr_2 = val_pwr_2 | self.VAL_PWR_MGMT_2_STBY_XA
            val_pwr_2 = val_pwr_2 | self.VAL_PWR_MGMT_2_STBY_YA
            val_pwr_2 = val_pwr_2 | self.VAL_PWR_MGMT_2_STBY_ZA

        #disable Gyro sensor
        if gyro == False:
            val_pwr_2 = val_pwr_2 | self.VAL_PWR_MGMT_2_STBY_XG
            val_pwr_2 = val_pwr_2 | self.VAL_PWR_MGMT_2_STBY_YG
            val_pwr_2 = val_pwr_2 | self.VAL_PWR_MGMT_2_STBY_ZG

        val_pwr_1 = 0x00
        #disable temp sensor
        if temp == False:
            val_pwr_1 = val_pwr_1 | self.VAL_PWR_MGMT_1_OFF_TEMP

        #cycle mode
        if cycle == True:
            val_pwr_1 = val_pwr_1 | self.VAL_PWR_MGMT_1_ON_CYCLE
            val_pwr_2 = val_pwr_2 | cycleFreq

        self.sendCmd( self.REG_PWR_MGMT_2, val_pwr_2 )
        self.sendCmd( self.REG_PWR_MGMT_1, val_pwr_1 )

    def openOnlyAccel(self, cycleFreq = 0x00 ):
        """Trun on device into Accelerometer Only Low Power Mode
        the [cycleFreq] value can be choise: 
            VAL_PWR_MGMT_2_LP_WAKE_CTRL_1_25HZ is default
            VAL_PWR_MGMT_2_LP_WAKE_CTRL_5HZ
            VAL_PWR_MGMT_2_LP_WAKE_CTRL_20HZ
            VAL_PWR_MGMT_2_LP_WAKE_CTRL_40HZ
        """
        self.openWith(accel = True, gyro = False, temp = False, cycle = True, cycleFreq = cycleFreq)

    def sleep(self):
        """Set device into sleep mode
        """
        self.sendCmd(self.REG_PWR_MGMT_1, self.VAL_PWR_MGMT_1_SLEEP)

    def setMotionInt(self, mot_dhpf = 0x01, mot_thr = 0x14, mot_dur = 0x30, mot_dete_dec = 0x15 ):
        """Set to enable Motion Detection Interrupt

            mot_dhpf        : set the Digital High Pass Filter. default is 0x01 - 5Hz
            mot_thr         : desired motion threshold. for example 20 (0x14), is default value
            mot_dur         : desired motion duration. for example 48ms (0x30), is default value
            mot_dete_dec    : motion detection decrement. for example 21 (0x15), is defaule value
        """
        #After power on (0x00 to register (decimal) 107), the Motion Detection Interrupt can be enabled as follows:
        #self.sendCmd( self.REG_PWR_MGMT_1, 0x00 )
        #(optionally?) Reset all internal signal paths in the MPU-6050 by writing 0x07 to register 0x68;
        self.sendCmd( self.REG_SIGNAL_PATH_RESET, 0x07 )
        #write register 0x37 to select how to use the interrupt pin. 
        #For an active high, push-pull signal that stays until register 
        #(decimal) 58 is read, write 0x20 (need read to clear INT state) or 0x00 (auto clear INT state).
        self.sendCmd( self.REG_INT_PIN_CFG, 0x00 )
        
        orgAccelConf = self.readByte(self.REG_ACCEL_CONFIG)
        newAccelConf = ( (orgAccelConf | 0xE7) ^ 0xE7 ) | mot_dhpf
        # Write register 28 (==0x1C) to set the Digital High Pass Filter, 
        # bits 3:0. For example set it to 0x01 for 5Hz. 
        # (These 3 bits are grey in the data sheet, but they are used! 
        # Leaving them 0 means the filter always outputs 0.)
        #
        # 0x00: RESET,
        # 0x01: 5Hz,
        # 0x02: 2.5Hz,
        # 0x03: 1.25Hz,
        # 0x04: 0.63Hz,
        # 0x07:hold
        #
        # 高通滤波器灵敏度调节
        #
        self.sendCmd( self.REG_ACCEL_CONFIG, newAccelConf )
        #Write the desired Motion threshold to register 0x1F (For example, write decimal 20).
        self.sendCmd( self.REG_MOTION_DET, mot_thr )
        #To register 0x20 (hex), write the desired motion duration, for example 40ms (0x28).
        # 灵敏度调节
        self.sendCmd( self.REG_MOTION_DET_DUR, mot_dur )
        
        #to register 0x69, write the motion detection decrement and 
        #a few other settings (for example write 0x15 to set both 
        #free-fall and motion decrements to 1 and accelerome0x00ter 
        #start-up delay to 5ms total by adding 1ms. )
        self.sendCmd( self.REG_MOTION_DET_CTRL, mot_dete_dec )

        #write register 0x38, bit 6 (0x40), to enable motion detection interrupt.
        self.sendCmd( self.REG_INT_ENABLE, self.VAL_INT_ENABLE_MOTION )

    def setDataRdyInt(self, int_cfg = 0x20 ):
        """Set to enabled Data Ready Interrupt
            int_cfg : Register 55( 0x37 ) – INT Pin / Bypass Enable Configuration, page 26
        """
        self.sendCmd( self.REG_INT_PIN_CFG, int_cfg )
        self.sendCmd( self.REG_INT_ENABLE, self.VAL_INT_ENABLE_DATA_RDY)

    def disableInt(self):
        """Trun Off Interrupt
        """
        self.sendCmd( self.REG_INT_ENABLE, self.VAL_INT_ENABLE_DISABLED )

    def getIntDataRdy(self):
        """Read INT status ( data ready, motion detect, etc. ) and clear INT status after readed
        
        MPU-6050 Register Map and Descriptions revision 4.2, page 28 -- Register 58(0x3A) – Interrupt Status
        """
        return self.readByte( self.REG_INT_STATUS )

    def getTemp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.
            Returns the temperature in degrees Celcius.
        """
        rawTemp = self.readWord( self.REG_TEMP_OUT_H )
        return (rawTemp + 12412.0) / 340.0
        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        # Temperature in degrees C = (TEMP_OUT Register Value as a signed quantity)/340 + 36.53
#         return ( rawTemp / 340.0 ) + 36.53

    def setAccelRange(self, accelRange):
        """Sets the range of the accelerometer to range.

        accelRange -- the range to set the accelerometer to. 
        Using a pre-defined range is advised.
        """
        self.sendCmd( self.REG_ACCEL_CONFIG, accelRange )

    def readAccelRange( self ):
        """Reads the range the accelerometer is set to.

        If raw is True, it will return the raw value from the ACCEL_CONFIG register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        raw_data = self.readByte(self.REG_ACCEL_CONFIG)
        raw_data = (raw_data | 0xE7) ^ 0xE7
        return raw_data

    def getAccelData( self,  raw = False ):
        """Gets and returns the X, Y and Z values from the accelerometer.

        If raw is True, it will return the data in m/s^2
        If raw is False, it will return the data in g
        Returns a dictionary with the measurement results.
        """
        x = self.readWord(self.REG_ACCEL_XOUT_H)
        y = self.readWord(self.REG_ACCEL_YOUT_H)
        z = self.readWord(self.REG_ACCEL_ZOUT_H)

        accel_scale_modifier = None
        accel_range = self.readAccelRange()

        if accel_range == self.ACCEL_RANGE_2G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            print( "Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G " )
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if raw == True:
            return { 'x': x, 'y': y, 'z': z }
        elif raw == False:
            return { 'x': x * self._gravityFactor, 'y': y * self._gravityFactor, 'z': z * self._gravityFactor }

    def setGyroRange(self, gyroRange):
        """Sets the range of the gyroscope to range.
        gyroRange -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
        """
        self.sendCmd( self.REG_GYRO_CONFIG, gyroRange )

    def readGyroRange( self ):
        """Reads the range the gyroscope is set to.

        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        """
        raw_data = self.readByte( self.REG_GYRO_CONFIG )
        raw_data = (raw_data | 0xE7) ^ 0xE7
        return raw_data

    def getGyroData(self):
        """Gets and returns the X, Y and Z values from the gyroscope.
        Returns the read values in a dictionary.
        """
        x = self.readWord(self.REG_GYRO_XOUT_H)
        y = self.readWord(self.REG_GYRO_YOUT_H)
        z = self.readWord(self.REG_GYRO_ZOUT_H)

        gyro_scale_modifier = None
        gyro_range = self.readGyroRange()

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier
        return {'x': x, 'y': y, 'z': z}

    def getAllData(self, temp = True, accel = True, gyro = True):
        """Reads and returns all the available data."""
        allData = {}
        if temp:
            allData["temp"] = self.getTemp()

        if accel:
            allData["accel"] = self.getAccelData( raw = False )

        if gyro:
            allData["gyro"] = self.getGyroData()

        return allData

if __name__ == "__main__":
    mpu = mpu6050( DEF_MPU6050_ADDRESS )
    print("REG_PWR_MGMT_1: {:#4x}".format(mpu.readByte(mpu.REG_PWR_MGMT_1)))
#     mpu.reset()
    mpu.setAccelRange( mpu.ACCEL_RANGE_2G )
    mpu.open()
    print("REG_PWR_MGMT_1: {:#4x}".format(mpu.readByte(mpu.REG_PWR_MGMT_1)))
    print("Accel Range: {:#4x} -- {:d}g".format(mpu.readAccelRange(), mpu.readAccelRange()))
    print("Gryo Range: {:#4x}".format(mpu.readGyroRange()))

    print (mpu.getAccelData( False ))
    print ("---------------------")

    allData = mpu.getAllData()
    print (allData)
    mpu.sleep()
