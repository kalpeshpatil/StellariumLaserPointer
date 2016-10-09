#!/usr/bin/python
import calendar
import datetime
import time
from astropy.time import Time
from numpy import sin, cos, arcsin, arctan2, pi

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

#Gets local time in given format
def get_current_local_time():
        local = datetime.datetime.now()
        print "Local:", local.strftime(TIME_FORMAT)


#Gets UTC time in given format
def get_current_utc_time():
        utc = datetime.datetime.utcnow()
        print "UTC:", utc.strftime(TIME_FORMAT)


#Converts local time to UTC time
def local_2_utc():
        local = datetime.datetime.now().strftime(TIME_FORMAT)
        print "local_2_utc: before convert:", local
        timestamp =  str(time.mktime(datetime.datetime.strptime(local, TIME_FORMAT).timetuple()) )[:-2]
        utc = datetime.datetime.utcfromtimestamp(int(timestamp))
        print "local_2_utc: after convert:", utc
        return utc


#Converts UTC time to local time
def utc_2_local():
        utc = datetime.datetime.utcnow().strftime(TIME_FORMAT)
        print "utc_2_local: before convert:", utc
        timestamp =  calendar.timegm((datetime.datetime.strptime( utc, TIME_FORMAT)).timetuple())
        local = datetime.datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
        print "utc_2_local: after convert:", local


def RADec2AzEl(RA,Dec,Lat,Lon,Alt): ##[Az El]

	# [Az El] = RADec2AzEl(350.858,58.8,'1991/05/19 13:00:00',50,10,0)
	#
	# Input Description:
	# RA    Right ascension (J2000) of sky position in degrees (0:360)
	# Dec   Declination angle (J2000) of sky position in degrees (-90:90)
	# UTC   Coordinated Universal Time YYYY/MM/DD hh:mm:ss
	# Lat   Latitude of location in degrees -90:90 -> S(-) N(+)
	# Lon   Longitude of location in degrees -180:180 W(-) E(+)
	# Alt   Altitude of location above sea level (km)
	#
	# Output Description:
	# Az    Azimuth angle of position in degrees (0:360)
	# El    Elevation angle of position in degrees (-90:90)
	
	# Compute JD
	TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
	utc_time = datetime.datetime.utcnow().strftime(TIME_FORMAT)
	# print type(utc_time)
	# print utc_time
	utc_time = '2016-04-11 12:51:24'

	t = Time(utc_time, scale='utc')
	# jd = juliandate(UTC,'yyyy/mm/dd HH:MM:SS');
	jd = t.jd1
	d = jd-2451543.5

	# Keplerian Elements for the Sun (geocentric)
	w = 282.9404+4.70935e-5*d            # longitude of perihelion degrees
	M = (356.0470+0.9856002585*d)%360 # mean anomaly degrees
	L = w + M                            # Sun's mean longitude degrees

	# Find the J2000 value
	J2000 = jd - 2451545.0

	utc_time1 = utc_time.split(':')
	utc_time2 = utc_time1[0].split(' ')

	UTH = float(utc_time2[1]) + float(utc_time1[1])/60 + float(utc_time1[2])/3600

	# Calculate local siderial time
	GMST0 = ((L+180)%360)/15
	SIDTIME = GMST0 + UTH + Lon/15

	# Replace RA with hour angle HA
	HA = (SIDTIME*15 - RA)

	# Convert to rectangular coordinate system
	x = cos(HA*(pi/180))*cos(Dec*(pi/180))
	y = sin(HA*(pi/180))*cos(Dec*(pi/180))
	z = sin(Dec*(pi/180))

	# Rotate this along an axis going east-west.
	xhor = x*cos((90-Lat)*(pi/180))-z*sin((90-Lat)*(pi/180))
	yhor = y
	zhor = x*sin((90-Lat)*(pi/180))+z*cos((90-Lat)*(pi/180))

	# Find the h and AZ 
	Az = arctan2(yhor,xhor)*(180/pi) + 180
	El = arcsin(zhor)*(180/pi)

	# logging.debug("Alt Az Regulus: '%s','%s'" % (El, Az))

	return Az, El

if __name__ == '__main__':
	RA = 21.625*360/24
	Dec = -11.7477
	Lon = 72.82
	Lat = 18.
	Alt = 0.01
	Az, El = RADec2AzEl(RA,Dec,Lat,Lon,Alt)
	print Az, El