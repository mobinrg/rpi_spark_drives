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
#    RPi-Spark Tone
#    @author Kunpeng Zhang
#    v1.0.0    2018.5.29
#

import RPi.GPIO as GPIO
from time import sleep
from time import time

TONE_A = 0
TONE_B = 1
TONE_C = 2
TONE_D = 3
TONE_E = 4
TONE_F = 5
TONE_G = 6

# /*
#     1b    2b    3b    4b    5b    6b    7b
# A    221    248    278    294    330    371    416
# B    248    278    294    330    371    416    467
# C    131    147    165    175    196    221    248
# D    147    165    175    196    221    248    278
# E    165    175    196    221    248    278    312
# F    175    196    221    234    262    294    330
# G    196    221    234    262    294    330    371
# */
TONE_BASS = [
  [221,248,278,294,330,371,416],
  [248,278,294,330,371,416,467],
  [131,147,165,175,196,221,248],
  [147,165,175,196,221,248,278],
  [165,175,196,221,248,278,312],
  [175,196,221,234,262,294,330],
  [196,221,234,262,294,330,371]
]

# /*
#     1      2     3     4     5     6     7
# A    441    495    556    589    661    742    833
# B    495    556    624    661    742    833    935
# C    262    294    330    350    393    441    495
# D    294    330    350    393    441    495    556
# E    330    350    393    441    495    556    624
# F    350    393    441    495    556    624    661
# G    393    441    495    556    624    661    742
# */
TONE_MID = [
  [441,495,556,589,661,742,833],
  [495,556,624,661,742,833,935],
  [262,294,330,350,393,441,495],
  [294,330,350,393,441,495,556],
  [330,350,393,441,495,556,624],
  [350,393,441,495,556,624,661],
  [393,441,495,556,624,661,742]
]

# /*
#     1#    2#    3#    4#    5#    6#    7#
# A  882  990    1112  1178  1322  1484  1665
# B  990  1112   1178  1322  1484  1665  1869
# C  525  589    661    700  786    882  990
# D  589  661    700    786  882    990  1112
# E  661  700    786    882  990    1112  1248
# F  700  786    882    935  1049  1178  1322
# G  786  882    990    1049  1178  1322  1484
# */
TONE_TREBLE = [
  [882,990,1112,1178,1322,1484,1665],
  [990,1112,1178,1322,1484,1665,1869],
  [525,589,661,700,786,882,990],
  [589,661,700,786,882,990,1112],
  [661,700,786,882,990,1112,1248],
  [700,786,882,935,1049,1178,1322],
  [786,882,990,1049,1178,1322,1484]
]

class RPiTonePlayer:
    """!
    \~english Use PWM to play tones
    \~chinese 使用PWM播放音符
    """
    TONE_DUTY = None
    MUTE_TONE = 0

    _pinPWM = None
    _pwmPlayer = None

    def __init__(self, pinPWM = None, toneDuty = 20):
        """!
        \~english
        Initialize the RPiTonePlayer object instance.
        @param pinPWM: This is a GPIO number of PWM for output
        @param toneDuty: The width of the pulse, 
                         its value can be chosen: 5 ~ 60
        @note on Raspberry Pi pwm output io you can be chosen in (BCM Mode): 12, 13, 18

        \~chinese
        初始化 RPiTonePlayer 对象实例
        @param pinPWM: 输出的 PWM 的 GPIO IO 编号
        @param toneDuty: 控制脉冲的宽度, 取值： 5 ~ 50
        @note 树莓派 pwm 输出可以选择（BCM模式）：12,13,18
        """
        self._pinPWM = pinPWM

        if toneDuty>50:
            self.TONE_DUTY = 50
        elif toneDuty<5:
            self.TONE_DUTY = 5
        else:
            self.TONE_DUTY = toneDuty

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pinPWM, GPIO.OUT)

    def _initPWMPlayer(self, freq):
        self._pwmPlayer = GPIO.PWM(self._pinPWM, freq)  # channel=12 frequency=50Hz
        #self._pwmPlayer.start(self.TONE_DUTY)
        #self._pwmPlayer.stop()

    def _delay(self, delay = 0):
        startTime=time()
        while True: 
            if (time() - startTime) > delay: break

    def stopTone(self):
        """!
        \~english Stop tone play
        \~chinese Stop tone play
        """
        if self._pwmPlayer == None: return False
        self._pwmPlayer.stop()

    def playTone(self, freq, reps = 1, delay = 0.1, muteDelay = 0.0):
        """!
        \~english Play a tone
        \~chinese 播放音符
        \~english 
        @param freq
        @param reps
        @param delay >= 0(s) if 0 means do not delay. tone play will be Stop immediately <br>
        @param muteDelay >= 0(s) If 0 means no pause after playing, play the next note immediately
        \~chinese 
        @param freq: 频率
        @param reps: 重复次数
        @param delay >= 0(s) 如果是 0 意味着不延迟。 音符会立即停止播放 <br>
        @param muteDelay >= 0(s) 如果是 0 表示音符播放结束后没有停顿，立刻播放下一个音符
        """
        if freq == 0: 
            self.stopTone()
            self._delay(delay)
            #sleep(delay)
            return False

        if self._pwmPlayer == None: self._initPWMPlayer(freq)

        for r in range(0,reps):
            self._pwmPlayer.start(self.TONE_DUTY)
            self._pwmPlayer.ChangeFrequency( freq )
            self._delay(delay)
            #sleep(delay)

            if muteDelay>0:
                self.stopTone()
                self._delay(muteDelay)
                #sleep(muteDelay)

        return True

    def playToneList(self, playList = None):
        """!
        \~english
        Play tone from a tone list
        @param playList a array of tones
        
        \~chinese
        播放音调列表
        @param playList: 音调数组
        
        \~english @note <b>playList</b> format:\n
        \~chinese @note <b>playList</b> 格式:\n
        \~
            <pre>
            [
              {"freq": 440, "reps": 1, "delay": 0.08, "muteDelay": 0.15},
              {"freq": 567, "reps": 3, "delay": 0.08, "muteDelay": 0.15},
              ...
            ]
           </pre>\n
        \~english
        \e delay: >= 0(s) if 0 means do not delay. tone play will be Stop immediately <br>
        \e muteDelay: 0.15 >= 0(s) If 0 means no pause after playing, play the next note immediately
        \~chinese
        \e delay: >= 0（s）如果是 0 意味着不延迟。 音调会立即停止播放 <br>
        \e muteDelay: >= 0（s）如果是 0 表示播放音符结束后没有停顿，立刻播放下一个音符
        """
        if playList == None: return False
        for t in playList:
            self.playTone(t["freq"], t["reps"], t["delay"], t["muteDelay"])

        self.stopTone()
        return True