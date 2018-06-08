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
#    RPi Spark Tone
#    by Kunpeng Zhang
#    v1.0.0    2018.5.29
#

import RPi.GPIO as GPIO
from time import sleep

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

class JMRPiTonePlayer:
    TONE_DUTY = 50
    MUTE_TONE = 0

    _pinPWM = None
    _pwmPlayer = None

    def __init__(self, pinPwm = None):
        self._pinPWM = pinPwm
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pinPWM, GPIO.OUT)

    def _initPWMPlayer(self, freq):
        self._pwmPlayer = GPIO.PWM(self._pinPWM, freq)  # channel=12 frequency=50Hz
        self._pwmPlayer.start(self.TONE_DUTY)
        self._pwmPlayer.stop()

    def stopTone(self):
        if self._pwmPlayer == None: return False
        self._pwmPlayer.stop()

    def playTone(self, freq, reps = 1, delay = 0.1, muteDelay = 0.0):
        if freq == 0: 
            self.stopTone()
            sleep(delay)
            return False

        if self._pwmPlayer == None: self._initPWMPlayer(freq)

        for r in range(0,reps):
            self._pwmPlayer.start(self.TONE_DUTY)
            self._pwmPlayer.ChangeFrequency( freq )
            sleep(delay)

            if muteDelay>0:
                self.stopTone()
                sleep(muteDelay)

        return True

    #############################################3
    # Play tone from a list
    # Item str of list:
    #    freq
    #    reps
    #    delay    >= 0(ms)    if 0 mean is do not delay. tone play will be Stop immediately 
    #    muteDelay >=0(ms)    if 0 mean is do not stop tone play.
    #
    def playToneList(self, playList = None):
        if playList == None: return False
        for t in playList:
            self.playTone(t["freq"], t["reps"], t["delay"], t["muteDelay"])

        self.stopTone()
        return True