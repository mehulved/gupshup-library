import simplejson as sj
import urllib
import connect
import sys

"""
Library to get message from text file and post it to SMS Gupshup
"""
def getMsg():
	"""
	Reads the message from the text file and returns it.
	"""
	msgOpen = open('msgFile.txt', 'r')
	msg = msgOpen.read()
	msg = msg.replace(" ", "+")
	msg = msg.replace("\n","+")
	return msg

def postMsg(msg, groupname, token, apiVersion):
	"""
	Post the retrived message to SMS Gupshup
	"""
	postMsgUrl = "http://api.smsgupshup.com/GupshupAPI/rest?text=%s&token=%s&groupName=%s&method=groups.postMessage&v=%s" % (msg, token, groupname, apiVersion)
	postMsgResult = sj.load(urllib.urlopen(postMsgUrl))

	if "status" in postMsgResult['response']:
		print "Your message was successfully posted."
	else:
		print postMsgResult['response']['error']['msg']
		sys.exit()
	
