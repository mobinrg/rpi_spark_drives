#
# RPi-Spark pHAT Drives
# Author: Kunpeng Zhang
# 2018.6.6
#

from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 4 - Beta',
	'Operating System :: POSIX :: Linux',
	'License :: OSI Approved :: MIT License',
	'Intended Audience :: Developers',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Topic :: Software Development',
	'Topic :: System :: Hardware',
	'Topic :: System :: Hardware :: Hardware Drivers'
]

keywords = (
	"development kit"
	"oled"
	"monochrome greyscale color"
	"ssd1306"
	"mpu6050"
	"attitude shake motion gyroscope accelerometer thermometer sensor"
	"spi i2c 128x64"
	"key buttons"
	"joystick game"
	"audio speaker headset headphone earphone"
	"pwm tone"
	"ogg mp3 wave"
	"gpio extended pads"
)

desc = 'The RPi-Spark pHat let you to easily develop interesting applications use the GPIO of Raspberry Pi. It included SSD1306 128x64 OLED, MPU6050 Sensor (Gyroscope, Accelerometer, Thermometer Sensor), 5 ways joystick, 2 push buttons, 3.5mm stereo headphone jack, Speaker and 19 extended GPIO pads'

setup (
	name              = 'JMRPi.Spark',
	version           = '1.0.9',
	author            = 'Kunpeng Zhang',
	author_email      = 'support@mobinrg.com',
	description       = desc,
	long_description  = desc,
	platforms		  = ['Linux'],
	license           = 'MIT',
	classifiers        = classifiers,
	keywords	  	  = keywords,
	url               = 'https://github.com/mobinrg/rpi_spark_drives',
	dependency_links  = [],
	install_requires  = [],
	packages          = find_packages()
)
