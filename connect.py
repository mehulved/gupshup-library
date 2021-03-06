#!/usr/bin/env python

"""
Library for connecting and disconnecting from SMS Gupshup.
"""
import simplejson as sj
import urllib
import hashlib
import base64
import sys


def getChallenge(apiVersion):
	"""
	Get challenge and salt from Gupshup API.
	Returns challenge and salt
	"""
	challengeUrl = "http://api.smsgupshup.com/GupshupAPI/rest?method=users.getChallenge&v=%s" % apiVersion
	challengeResult = sj.load(urllib.urlopen(challengeUrl))
	
	if "status" in challengeResult['response']:
		salt = challengeResult['response']['salt']
		challenge = challengeResult['response']['challenge']
		print "Got challenge"
		return salt, challenge
	else:
		print challengeResult['response']['error']['msg']
		sys.exit()

def tryLogin(salt, challenge, password, phoneno, apiVersion, countryCode):	
	"""
	Login to SMS Gupshup.
	Returns the login token.
	"""
	status = validate(phoneno, countryCode)
	salt, challenge = getChallenge(phoneno, password, apiVersion, countryCode)

	rand = base64.b64encode(hashlib.md5(base64.b64encode(hashlib.md5(password+salt).digest())+challenge).digest())
	# workaround way to deal with urlencode in python since it requires a tuple
	tmp = urllib.urlencode({'x': rand})
	rand = tmp[2:]

	loginUrl = "http://api.smsgupshup.com/GupshupAPI/rest?phone=%s&rand=%s&countryCode=%s&challenge=%s&method=users.login&v=%s" % (phoneno, rand, countryCode, challenge, apiVersion)
	loginResult = sj.load(urllib.urlopen(loginUrl))
	
	if "status" in loginResult['response']:
		print "Login Successful"
		token = loginResult['response']['token']
		return token
	else:
		print loginResult['response']['error']['msg']
		sys.exit()

def tryLogout(token, apiVersion):
	logoutUrl = "http://api.smsgupshup.com/GupshupAPI/rest?token=%s&method=users.logout&v=%s" % (token,apiVersion)
	logoutRequest = sj.load(urllib.urlopen(logoutUrl))

	if "status" in logoutRequest['response']:
		print "Logout Successful"
	else:
		print logoutRequest['response']['error']['msg']
		sys.exit()

def validate(phoneno, countryCode):
	"""
	Validate the phone number and country code before proceeding with the login process
	"""
	status = False
	if (countryCode == "91"):
		status = True
	
	if (len(phoneno) == 10):
		status = True

	return status

