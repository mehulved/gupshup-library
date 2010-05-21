#!/usr/bin/env python

"""
Library for connecting and disconnecting from SMS Gupshup.
"""
import iniparse
import simplejson as sj
import urllib
import hashlib
import base64
import sys

global token

class gsconnect:

	def __init__(self):
		salt, challenge = self.getChallenge()
		cfg = iniparse.INIConfig(open('settings.ini'))
		password = cfg['sms']['password']
		phoneno = cfg['sms']['phoneno']
		token = self.tryLogin(salt, challenge, password, phoneno)
		
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

class gsdisconnect:

	def __init__(self):
		self.tryLogout(token)

	def tryLogout(self,token):
		logoutUrl = "http://api.smsgupshup.com/GupshupAPI/rest?token=%s&method=users.logout&v=%s" % (token,apiVersion)
		logoutResponse = js.load(urllib.urlopen(logoutUrl))

		if "status" in lougoutRequest['response']:
			print "Logout Successful"
		else:
			print logoutRequest['response']['error']['msg']
			sys.exit()
