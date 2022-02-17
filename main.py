from machine import Pin, SPI
from machine import RTC, Timer
import machine,time, _thread, math, sys
import os, network, gc, ubinascii
from wifi import *
from ntptime import settime
import ili9342c

import vga1_8x8 as font1
import vga1_8x16 as font2
import vga1_16x32 as font3
#import vga2_8x8 as font4
#import vga2_8x16 as font5
#import vga2_16x16 as font6
#import vga2_16x32 as font7
tft = ili9342c.ILI9342C(
            SPI(2, baudrate=60000000, sck=Pin(18), mosi=Pin(23)),
            240,
            320,
            reset=Pin(33, Pin.OUT),
            cs=Pin(26, Pin.OUT),
            dc=Pin(5, Pin.OUT),
            backlight=Pin(32, Pin.OUT),
            rotation=6,
            buffer_size=16*32*2)
tft.init()
tft.inversion_mode(False)
tft.fill(ili9342c.BLUE)
time.sleep(1)
wifi()
from ntptime import settime
settime()
ctime=truetime_calc()
#rtc = RTC()
# ist von loloris noch zu übernehmen
#rtc.ntp_sync(server='de.pool.ntp.org',tz='CET-1CEST,M3.5.0,M10.5.0/3')
sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)
#ap_if.active(True)
ap_if.active(False)
tft.fill(ili9342c.BLUE)
tft.text(font2,'{:02d}:{:02d}:{:02d}'.format(ctime[3],ctime[4],ctime[5]),0,0, ili9342c.WHITE, ili9342c.BLUE)
tft.text(font2,'{:02d}:{:02d}:{:04d}'.format(ctime[2],ctime[2],ctime[0]),158,0, ili9342c.WHITE, ili9342c.BLUE)
#
tft.text(font2,'Network & Systeminfo',0,20, ili9342c.YELLOW, ili9342c.BLUE)
tft.text(font2,'CL MAC  : {}'.format(ubinascii.hexlify(sta_if.config('mac'),':').decode()),0,40, ili9342c.GREEN , ili9342c.BLUE)
tft.text(font2,'AP MAC  : {}'.format(ubinascii.hexlify(ap_if.config('mac'),':').decode()),0,60, ili9342c.GREEN , ili9342c.BLUE)
tft.text(font2,'CL IP   : {}'.format(sta_if.ifconfig()[0]),0,80, ili9342c.GREEN , ili9342c.BLUE)
tft.text(font2,'CL MASK : {}'.format(sta_if.ifconfig()[1]),0,100, ili9342c.GREEN , ili9342c.BLUE)
tft.text(font2,'CL GW   : {}'.format(sta_if.ifconfig()[2]),0,120, ili9342c.GREEN , ili9342c.BLUE)
tft.text(font2,'CL NS   : {}'.format(sta_if.ifconfig()[3]),0,140, ili9342c.GREEN , ili9342c.BLUE)
if ap_if.active():
    tft.text(font2,'AP IP   : {}'.format(ap_if.ifconfig()[0]),0,160, ili9342c.YELLOW, ili9342c.BLUE)
    tft.text(font2,'AP MASK : {}'.format(ap_if.ifconfig()[1]),0,180, ili9342c.YELLOW, ili9342c.BLUE)
    tft.text(font2,'AP GW   : {}'.format(ap_if.ifconfig()[2]),0,200, ili9342c.YELLOW, ili9342c.BLUE)
    if ap_if.isconnected():
        tft.text(font2,'AP Connect :',0,220, ili9342c.WHITE, ili9342c.BLUE)
        tft.text(font2,'{}'.format(ap_if.isconnected()),100,220, ili9342c.GREEN, ili9342c.BLUE)
    else:
        tft.text(font2,'AP Connect :',0,220, ili9342c.YELLOW, ili9342c.BLUE)
        tft.text(font2,'{}'.format(ap_if.isconnected()),100,220, ili9342c.MAGENTA, ili9342c.BLUE)

else:
    mem_total = gc.mem_alloc()+gc.mem_free()
    free_percent = gc.mem_free()/mem_total*100.0
    alloc_percent = gc.mem_alloc()/mem_total*100.0
    tft.text(font2,'Memory'.format(ap_if.ifconfig()[0]),0,160, ili9342c.YELLOW, ili9342c.BLUE)
    tft.text(font2,'total : {} KB '.format(mem_total/1024),0,180, ili9342c.YELLOW, ili9342c.BLUE)
    tft.text(font2,'usage : {:4.2f} KB {:2.2f}%'.format(gc.mem_alloc()/1024,alloc_percent),0,200, ili9342c.YELLOW, ili9342c.BLUE)
    tft.text(font2,'free  : {:4.2f} KB {:2.2f}%'.format(gc.mem_free()/1024,free_percent),0,220, ili9342c.YELLOW, ili9342c.BLUE)
    pass
#tft.text(font2,'{}'.format(os.uname().machine),0,240, ili9342c.WHITE, ili9342c.BLUE)
tft.text(font2,'{}'.format(os.uname().machine).replace('ESP32 ',''),0,240, ili9342c.WHITE, ili9342c.BLUE)
tft.text(font2,'{}'.format(str(os.uname().version).replace('ESP32_','')),0,260, ili9342c.WHITE, ili9342c.BLUE)
tft.text(font2,'Python  : {}'.format(str(sys.version_info).replace(",",".").replace("(","").replace(")","").replace(" ","")),0,280, ili9342c.WHITE, ili9342c.BLUE)
tft.text(font2,'CPU frequency : {} Mhz'.format(machine.freq()/1000000),0,280, ili9342c.WHITE, ili9342c.BLUE)
# clock
'''
while True:
    ctime=truetime_calc()
    pt(ctime)
    tft.text(font2,'{:02d}:{:02d}:{:02d}'.format(ctime[3],ctime[4],ctime[5]),0,0, ili9342c.WHITE, ili9342c.BLUE)
    tft.text(font2,'{:02d}.{:02d}.{:04d}'.format(ctime[2],ctime[1],ctime[0]),158,0, ili9342c.WHITE, ili9342c.BLUE)
    time.sleep(1)
'''
