
#ipinfo is taken from ipinfo.io but its not working as expected
#import ipinfo
#geocoder provides more specific information
import geocoder
#user for getting user name
import getpass

def userName():
	username = getpass.getuser()
	return username

def geoCode():
	g = geocoder.ip('me')
	return g
