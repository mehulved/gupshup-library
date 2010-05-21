#!/usr/bin/env python

import iniparse
import simplejson as sj
import urllib
import hashlib
import base64
import sys

class gsconnect:

	def __init__(self):
		global countryCode 
		global apiVersion

		countryCode = "91"
		apiVersion = "1.0"

		salt, challenge = self.getChallenge()
		cfg = iniparse.INIConfig(open('settings.ini'))
		password = cfg['sms']['password']
		phoneno = cfg['sms']['phoneno']
		self.tryLogin(salt, challenge, password, phoneno)
		
	def getChallenge(self):
		"""
		Get challenge and salt from Gupshup API.
		Returns challenge and salt
		"""
		
		challengeUrl = "http://api.smsgupshup.com/GupshupAPI/rest?method=users.getChallenge&v=%s" % apiVersion
		challengeResult = sj.load(urllib.urlopen(challengeUrl))
		
		if "status" in challengeResult['response']:
			salt = challengeResult['response']['salt']
			challenge = challengeResult['response']['challenge']
			return salt, challenge
		else:
			print challengeResult['response']['error']['msg']
			sys.exit()

	def tryLogin(self, salt, challenge, password, phoneno):	
		"""
		Login to SMS Gupshup.
		Returns the login token.
		"""
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
