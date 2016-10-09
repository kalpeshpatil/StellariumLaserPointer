#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import re
import logging
from time import time, ctime, strftime, localtime
from RADec2AzEl import *


def rad_2_hour(rads):
    h = round( (rads * 180)/(15 * math.pi), 6)
    if h > 24.0:
        h = h - 24.0
    if h < 0.0:
        h = 24.0 + h
    return h

def radStr_2_deg(rad):
    exp = re.compile('^(-?)[0-9]{1}\.[0-9]{4,8}')
    
    if(not exp.match(rad)):
        return None
    
    r = float(rad)
    if(r < 0):
        r = (2 * math.pi) - abs(r)
    
    return (r * 180) / math.pi

def rad_2_radStr(rad):
    if(rad < 0.0): return '%f' % rad;
    else: return '+%f' % rad;
    
def radStr_2_degStr(r):
    return deg_2_degStr(radStr_2_deg(r))

def degStr_2_rad(d):
    exp1 = re.compile('^-?[0-9]{,3}(º|ᵒ)[0-9]{,3}\'[0-9]{,3}([\']{2}|")$')
    exp2 = re.compile('^-?[0-9]{,3}\.[0-9]{,6}(º|ᵒ)$')

    if(not exp1.match(d) and not exp2.match(d)):
        logging.debug("Error parametro: %s" % d)
        return None
    elif(exp1.match(d)):
        d = d.replace('º','.').replace("''",'.').replace("'",'.')
        d_dic = d.split('.')
        d_deg = float(d_dic[0])
        d_min = float(d_dic[1])
        d_sec = float(d_dic[2])
        
        if(d_deg < 0):
            d_min = 0 - d_min;
            d_sec = 0 - d_sec;
    
        d_ndeg = (d_deg+(d_min/60)+(d_sec/(60**2)))
    else:
        d_ndeg = float(d.replace('º',''))
        if(d_ndeg < 0): d_ndeg = 360 - abs(d_ndeg);

    return round((d_ndeg * math.pi) / 180, 6)

def degStr_2_radStr(d):
    return rad_2_radStr(degStr_2_rad(d))

def deg_2_degStr(deg):
    ndeg = math.floor(float(deg))
    
    nmins = (deg - ndeg) * 60
    mins = math.floor(nmins)
    secs = round( (nmins - mins) * 60 )
    
    return "%dº%d'%d''" % (ndeg, mins, secs)

def hourStr_2_rad(h):
    exp = re.compile('^[0-9]{,3}h[0-9]{,3}m[0-9]{,3}s$')
    if(not exp.match(h)):
        logging.debug("Error in param: %s" % h)
        return None
    
    h = h.replace('h','.').replace("m",'.').replace("s",'.')
    h_dic = h.split('.')

    h_h = float(h_dic[0])
    h_m = float(h_dic[1])
    h_s = float(h_dic[2])

    nh = (h_h+(h_m/60)+(h_s/(60**2)))

    return round((nh * 15 * math.pi) / 180, 6)
    
def hour_2_hourStr(hours):
    (h, m, s) = hour_min_sec(hours)
    return '%dh%dm%00.1fs' % (h, m, s)
    
def hour_min_sec(hours):
    h = math.floor(hours)
    
    hours_m = (hours - h)*60.0
    m = math.floor(hours_m)
    
    s = (hours_m - m)*60.0
    
    #Avoiding the X.60 values
    if s >= 59.99:
        s = 0
        m += 1
    if m >= 60:
        m = 60-m
        h += 1
    
    return (h, m, s)
    
def grad_min_sec(degs):
    #Avoiding operations with negative values
    to_neg = False
    if degs < 0:
        degs = math.fabs(degs)
        to_neg = True
    
    d = math.floor(degs)
    
    degs_m = (degs - d)*60.0
    m = math.floor(degs_m)
    
    s = (degs_m - m)*60.0
    
    #Avoiding the .60 values
    if s >= 59.99:
        s = 0
        m += 1
    if m >= 60.0:
        m = 60.0-m
        d += 1
    
    if to_neg:
        d = -d;
    
    return (d, m, s)

def eCoords2str(ra, dec, mtime):
    ra_h = ra*12.0/2147483648
    dec_d = dec*90.0/1073741824
    time_s = math.floor(mtime / 1000000)
    
    return ('%dh%dm%00.0fs' % hour_min_sec(ra_h), '%dº%d\'%00.0f\'\'' % grad_min_sec(dec_d), strftime("%Hh%Mm%Ss", localtime(time_s)))
    
def toJ2000(ra, dec, mtime):
   ra_h = ra*12.0/2147483648
    (h1, m1, s1) = hour_min_sec(ra_h)
        
    dec_d = dec*90.0/1073741824
    (h2, m2, s2) = grad_min_sec(dec_d)

    time_s = math.floor(mtime / 1000000)  # From microseconds to seconds (Unix timestamp)
    t = ctime(time_s)
            
    return '%dh%dm%00.0fs/%dº%d\'%00.1f\'\' at %s' % (h1, m1, s1, h2, m2, s2, t)
        

def rad_2_stellarium_protocol(ra, dec):
    Lon = 72.82
    Lat = 18.96
    Alt = 0.01

    ra_h = rad_2_hour(ra)
    
    dec_d = (dec * 180) / math.pi

    Az, El = RADec2AzEl(ra*180/math.pi,dec_d,Lat,Lon,Alt)

    logging.debug("(hours, degrees): (%f, %f)" % (ra_h, dec_d))
    logging.debug("(Az, Alt): (%f, %f)" % (Az, El))
    
    return (int(ra_h*(2147483648/12.0)), int(dec_d*(1073741824/90.0)))
    
