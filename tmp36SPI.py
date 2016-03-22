#!/usr/bin/python
#-*- coding: utf-8 -*-

#d an LM35 on CH0 of an MCP3008 on a Raspberry Pi
# mostly nicked from
#  http://jeremyblythe.blogspot.ca/2012/09/raspberry-pi-hardware-spi-analog-inputs.html

import spidev
import os
import glob
import time

spi = spidev.SpiDev()
spi.open(0, 0)

def readadc(adcnum):
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    return adcout

def generate_values(pipeout):
    while True:
        deg_c= readadc(0)
        print deg_c
        os.write(pipeout, b'%de' % (deg_c))
        time.sleep(0.1)
#generate_values()
named_pipe_path = '/dev/ttyTemperature'

if not os.path.exists(named_pipe_path):
    os.mkfifo(named_pipe_path)

pipeout = os.open(named_pipe_path, os.O_WRONLY)
generate_values(pipeout)
os.close(pipeout)
os.remove(named_pipe_path)
