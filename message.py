import simplejson as sj
import urllib
import connect
import sys
import iniparse

class sendMsg:
	
	def __init__(self):
		msg = self.getMsg()
		cfg = INIConfig()
		groupname = cfg['sms']['groupname']
		postMsg(msg, groupname)

	def getMsg(self):
		"""
		Reads the message from the text file and returns it.
		"""
		msgOpen = open('msgFile.txt', 'r')
		msg = msgOpen.read()
		msg = msg.replace(" ", "+")
		return msg

	def postMsg(self, msg, groupname):
		"""
		Post the retrived message to SMS Gupshup
		"""
		postMsgUrl = "http://api.smsgupshup.com/rest?text=%s&token=%s&groupName=%s&method=groups.postMessage&v=%s" % (msg, token, groupname, apiVersion)
		postMsgResult = sj.load(urllib.urlopen(postMsgUrl))

		if "status" in postMsgResult['response']:
			print "Your message was successfully posted."
		else:
			print postMsgResult['response']['error']['msg']
			sys.exit()
		
