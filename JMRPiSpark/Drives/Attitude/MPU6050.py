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
# @author: Kunpeng Zhang
# @version v1.0.0
# @date 2018.04.01
#

import smbus

##
# default I2C address of MPU6050
DEF_MPU6050_ADDRESS = 0x68

##
# Earth Gravitiy
GRAVITIY_EARTH  = 9.80665

class MPU6050:
    """!
    \~english
    This driver is for MPU-6050 Motion Processing Unit( InvenSense Inc ).

    Features: <br>
        * Gyroscope sensor
        * Accelerometer sensor
        * Temperature sensor
        * Sensor data ready Interrupt
        * Motion detection Interrupt
        * Sleep mode
        * More...

    \~chinese
    此驱动程序适用于MPU-6050运动处理单元 ( InvenSense Inc )。

         特点：<br>
             * 陀螺仪
             * 加速度计
             * 温度传感器
             * 传感器数据就绪中断
             * 移动侦测中断
             * 睡眠模式
             * 更多...
    """

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1KDEG = 32.8
    GYRO_SCALE_MODIFIER_2KDEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1KDEG  = 0x10
    GYRO_RANGE_2KDEG  = 0x18

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
    _gravityFactor = None;

    def __init__(self, address, busId = 1, gravityFactor = GRAVITIY_EARTH ):
        """!
        \~english
        Initialize the MPU6050 object instance

        @param address        MPU6050 I2C Address (default is: 0x68)
        @param busId          I2C Bus ID of Raspberry Pi. RPi-Spark pHAT default is 1
        @param gravityFactor  Default is GRAVITIY_EARTH
        
        \~chinese
        初始化 MPU6050 实例

        @param address        MPU6050 I2C 地址（默认为：0x68）
        @param busId          树梅派( Raspberry Pi ) I2C 总线 ID。 RPi-Spark pHAT 默认值为 1
        @param gravityFactor  默认 GRAVITIY_EARTH ( 地球重力加速度 )

        \~ \n
        @see DEF_MPU6050_ADDRESS
        @see GRAVITIY_EARTH
        """
        self._address = address
        self._bus = smbus.SMBus( busId )
        self._gravityFactor = gravityFactor
        self.setAccelRange( self.ACCEL_RANGE_2G )

    def _readByte(self, regAddr):
        return self._bus.read_byte_data(self._address, regAddr)

    def _readWord(self, regAddr):
        high = self._readByte(regAddr)
        low = self._readByte(regAddr+1)
        rawVal = ( high << 8 ) | low;
        if (rawVal >= 0x8000):
            return -((65535 - rawVal) + 1)
        else:
            return rawVal

    def _writeByte(self, regAddr, regValue):
        self._bus.write_byte_data(self._address, regAddr, regValue)

    def _sendCmd(self, cmd, value, firstClear = True):
        if firstClear:
            self._writeByte(cmd, 0x00)
        self._writeByte(cmd, value)

    def reset(self):
        """!
        \~english Reset MPU all registers
        \~chinese 复位全部寄存器
        """
        self._writeByte(self.REG_PWR_MGMT_1, self.VAL_PWR_MGMT_1_RESET)
 
    def open(self):
        """!
        \~english Trun on device and with all sensors at same time
        \~chinese 开启全部传感器
        """
        self._sendCmd(self.REG_PWR_MGMT_1, 0x00)
        self._sendCmd(self.REG_PWR_MGMT_2, 0x00)

    def openWith(self, accel = True, gyro = True, temp = True, cycle = False, cycleFreq = 0x00):
        """!
        Trun on device with configurable sensors into wake up mode
        
        @param accel: True - Enable accelerometer
        @param gyro: True - Enable gyroscope
        @param temp: True - Enable Thermometer
        @param cycle: True - Enable cycle wake-up mode
        @param cycleFreq: Cycle wake-up frequency, this value can be chosen:

          @see VAL_PWR_MGMT_2_LP_WAKE_CTRL_1_25HZ is default
          @see VAL_PWR_MGMT_2_LP_WAKE_CTRL_5HZ
          @see VAL_PWR_MGMT_2_LP_WAKE_CTRL_20HZ
          @see VAL_PWR_MGMT_2_LP_WAKE_CTRL_40HZ
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

        self._sendCmd( self.REG_PWR_MGMT_2, val_pwr_2 )
        self._sendCmd( self.REG_PWR_MGMT_1, val_pwr_1 )

    def openOnlyAccel(self, cycleFreq = 0x00 ):
        """!
        Trun on device into Accelerometer Only Low Power Mode
        @param cycleFreq can be choise: 
            @see VAL_PWR_MGMT_2_LP_WAKE_CTRL_1_25HZ is default
            @see VAL_PWR_MGMT_2_LP_WAKE_CTRL_5HZ
            @see VAL_PWR_MGMT_2_LP_WAKE_CTRL_20HZ
            @see VAL_PWR_MGMT_2_LP_WAKE_CTRL_40HZ
        """
        self.openWith(accel = True, gyro = False, temp = False, cycle = True, cycleFreq = cycleFreq)

    def sleep(self):
        """!
            \~english Set device into sleep mode
            \~chinese MPU6050 进入睡眠模式，低功耗
        """
        self._sendCmd(self.REG_PWR_MGMT_1, self.VAL_PWR_MGMT_1_SLEEP)

    def setMotionInt(self, motDHPF = 0x01, motTHR = 0x14, motDUR = 0x30, motDeteDec = 0x15 ):
        """!
        Set to enable Motion Detection Interrupt

        @param motDHPF Set the Digital High Pass Filter. Default is 0x01 (5Hz)
        @param motTHR  Desired motion threshold. Default is 20 (0x14)
        @param motDUR  Desired motion duration. Default is 48ms (0x30)
        @param motDeteDec Motion detection decrement. Default is 21 (0x15)
        
        @note <b>motDHPF</b> should be one of the following values:<br>
            0x00: RESET,<br>
            0x01: 5Hz,<br>
            0x02: 2.5Hz,<br>
            0x03: 1.25Hz,<br>
            0x04: 0.63Hz,<br>
            0x07: HOLD<br>
        """
        #After power on (0x00 to register (decimal) 107), the Motion Detection Interrupt can be enabled as follows:
        #self._sendCmd( self.REG_PWR_MGMT_1, 0x00 )
        #(optionally?) Reset all internal signal paths in the MPU-6050 by writing 0x07 to register 0x68;
        self._sendCmd( self.REG_SIGNAL_PATH_RESET, 0x07 )
        #write register 0x37 to select how to use the interrupt pin. 
        #For an active high, push-pull signal that stays until register 
        #(decimal) 58 is read, write 0x20 (need read to clear INT state) or 0x00 (auto clear INT state).
        self._sendCmd( self.REG_INT_PIN_CFG, 0x00 )
        
        orgAccelConf = self._readByte(self.REG_ACCEL_CONFIG)
        newAccelConf = ( (orgAccelConf | 0xE7) ^ 0xE7 ) | motDHPF
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
        # 0x07: hold
        #
        # 高通滤波器灵敏度调节
        #
        self._sendCmd( self.REG_ACCEL_CONFIG, newAccelConf )
        #Write the desired Motion threshold to register 0x1F (For example, write decimal 20).
        self._sendCmd( self.REG_MOTION_DET, motTHR )
        #To register 0x20 (hex), write the desired motion duration, for example 40ms (0x28).
        # 灵敏度调节
        self._sendCmd( self.REG_MOTION_DET_DUR, motDUR )
        
        #to register 0x69, write the motion detection decrement and 
        #a few other settings (for example write 0x15 to set both 
        #free-fall and motion decrements to 1 and accelerome0x00ter 
        #start-up delay to 5ms total by adding 1ms. )
        self._sendCmd( self.REG_MOTION_DET_CTRL, motDeteDec )

        #write register 0x38, bit 6 (0x40), to enable motion detection interrupt.
        self._sendCmd( self.REG_INT_ENABLE, self.VAL_INT_ENABLE_MOTION )

    def setDataRdyInt(self, int_cfg = 0x20 ):
        """!
        \~english 
        Set to enabled Data Ready Interrupt
        int_cfg : Register 55( 0x37 ) – INT Pin / Bypass Enable Configuration, page 26
        
        \~chinese 
        启用数据就绪中断
        @param int_cfg: 寄存器 55( 0x37 ) – INT Pin / Bypass Enable Configuration, page 26
        """
        self._sendCmd( self.REG_INT_PIN_CFG, int_cfg )
        self._sendCmd( self.REG_INT_ENABLE, self.VAL_INT_ENABLE_DATA_RDY)

    def disableInt(self):
        """!
            Trun Off Interrupt
        """
        self._sendCmd( self.REG_INT_ENABLE, self.VAL_INT_ENABLE_DISABLED )

    def getIntDataRdy(self):
        """!
        \~english
        Get data ready interrupt status (data ready, motion detection, etc.) 
        After calling this method the data ready interrupt flag will be reset, 
        waiting for the next data ready interrupt

        MPU6050 Register Map and Descriptions revision 4.2, page 28 
        Register 58(0x3A) – Interrupt Status
        \~chinese
        读取数据就绪中断状态（数据就绪，运动检测等），调用该方法后数据就绪中断标志位将复位，等待下一次数据就绪中断
        MPU6050寄存器映射和描述修订4.2，第28页
        寄存器58（0x3A）- 中断状态
        """
        return self._readByte( self.REG_INT_STATUS )

    def getTemp(self):
        """!
        \~english
        Reads the temperature from the onboard temperature sensor of the MPU-6050.
        @returns a float value, the temperature in degrees Celcius.
        @note MPU6050 Register Map and Descriptions revision 4.2, page 30
        \~chinese
        MPU-6050 的板载温度传感器读取温度
        @returns 浮点值，温度以摄氏度为单位
        @note MPU6050寄存器映射和描述修订4.2，第30页
        """
        rawTemp = self._readWord( self.REG_TEMP_OUT_H )
        return (rawTemp + 12412.0) / 340.0
        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        # Temperature in degrees C = (TEMP_OUT Register Value as a signed quantity)/340 + 36.53
#         return ( rawTemp / 340.0 ) + 36.53

    def setAccelRange(self, accelRange):
        """!
        Set range of accelerometer.
        @param accelRange: range of accelerometer.
          It should be one of the following values:
              @see ACCEL_RANGE_2G
              @see ACCEL_RANGE_4G
              @see ACCEL_RANGE_8G
              @see ACCEL_RANGE_16G
        @note Using a pre-defined range is advised.
        """
        self._sendCmd( self.REG_ACCEL_CONFIG, accelRange )

    def readAccelRange( self ):
        """!
        Reads the range of accelerometer setup.
        
        @return an int value.
          It should be one of the following values:
              @see ACCEL_RANGE_2G
              @see ACCEL_RANGE_4G
              @see ACCEL_RANGE_8G
              @see ACCEL_RANGE_16G
        """
        raw_data = self._readByte(self.REG_ACCEL_CONFIG)
        raw_data = (raw_data | 0xE7) ^ 0xE7
        return raw_data

    def getAccelData( self,  raw = False ):
        """!
        Gets and returns the X, Y and Z values from the accelerometer.

        @param raw If raw is True, it will return the data in m/s^2,<br> If raw is False, it will return the data in g
        @return a dictionary with the measurement results or Boolean.
            @retval {...} data in m/s^2 if raw is True.
            @retval {...} data in g if raw is False.
            @retval False means 'Unkown accel range', that you need to check the "accel range" configuration
        @note Result data format: {"x":0.45634,"y":0.2124,"z":1.334}
        """
        x = self._readWord(self.REG_ACCEL_XOUT_H)
        y = self._readWord(self.REG_ACCEL_YOUT_H)
        z = self._readWord(self.REG_ACCEL_ZOUT_H)

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
            print( "ERROR: Unkown accel range!" )
            return False            
            #accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if raw == True:
            return { 'x': x, 'y': y, 'z': z }
        elif raw == False:
            return { 'x': x * self._gravityFactor, 'y': y * self._gravityFactor, 'z': z * self._gravityFactor }

    def setGyroRange(self, gyroRange):
        """!
        Set range of gyroscope.
        @param gyroRange: range of gyroscope.
          It should be one of the following values:
              @see GYRO_RANGE_250DEG
              @see GYRO_RANGE_500DEG
              @see GYRO_RANGE_1KDEG
              @see GYRO_RANGE_2KDEG 

        @note Using a pre-defined range is advised.
        """
        self._sendCmd( self.REG_GYRO_CONFIG, gyroRange )

    def readGyroRange( self ):
        """!
        Read range of gyroscope.

        @return an int value. It should be one of the following values (GYRO_RANGE_250DEG)

        @see GYRO_RANGE_250DEG
        @see GYRO_RANGE_500DEG
        @see GYRO_RANGE_1KDEG
        @see GYRO_RANGE_2KDEG
        """
        raw_data = self._readByte( self.REG_GYRO_CONFIG )
        raw_data = (raw_data | 0xE7) ^ 0xE7
        return raw_data

    def getGyroData(self):
        """!
        Gets and returns the X, Y and Z values from the gyroscope

        @return a dictionary with the measurement results or Boolean.
            @retval {...} a dictionary data.
            @retval False means 'Unkown gyroscope range', that you need to check the "gyroscope range" configuration
        @note Result data format: {"x":0.45634,"y":0.2124,"z":1.334}
        """
        x = self._readWord(self.REG_GYRO_XOUT_H)
        y = self._readWord(self.REG_GYRO_YOUT_H)
        z = self._readWord(self.REG_GYRO_ZOUT_H)

        gyro_scale_modifier = None
        gyro_range = self.readGyroRange()

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1KDEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1KDEG
        elif gyro_range == self.GYRO_RANGE_2KDEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2KDEG
        else:
            print("ERROR: Unkown gyroscope range!")
            return False
            #gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier
        return {'x': x, 'y': y, 'z': z}


    def getAllData(self, temp = True, accel = True, gyro = True):
        """!
        Get all the available data.

        @param temp: True - Allow to return Temperature data
        @param accel: True - Allow to return Accelerometer data
        @param gyro: True - Allow to return Gyroscope data

        @return a dictionary data
            @retval {} Did not read any data
            @retval {"temp":32.3,"accel":{"x":0.45634,"y":0.2124,"z":1.334},"gyro":{"x":0.45634,"y":0.2124,"z":1.334}} Returned all data
        """
        allData = {}
        if temp:
            allData["temp"] = self.getTemp()

        if accel:
            allData["accel"] = self.getAccelData( raw = False )

        if gyro:
            allData["gyro"] = self.getGyroData()

        return allData

#
# This a simple test
# if __name__ == "__main__":
#     mpu = mpu6050( DEF_MPU6050_ADDRESS )
#     print("REG_PWR_MGMT_1: {:#4x}".format(mpu._readByte(mpu.REG_PWR_MGMT_1)))
# #     mpu.reset()
#     mpu.setAccelRange( mpu.ACCEL_RANGE_2G )
#     mpu.open()
#     print("REG_PWR_MGMT_1: {:#4x}".format(mpu._readByte(mpu.REG_PWR_MGMT_1)))
#     print("Accel Range: {:#4x} -- {:d}g".format(mpu.readAccelRange(), mpu.readAccelRange()))
#     print("Gryo Range: {:#4x}".format(mpu.readGyroRange()))
# 
#     print (mpu.getAccelData( False ))
#     print ("---------------------")
# 
#     allData = mpu.getAllData()
#     print (allData)
#     mpu.sleep()