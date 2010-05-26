#!/usr/bin/env python

from iniparse import INIConfig
import feed_handler
import connect
import message

cfg = INIConfig(open('settings.ini'))
rsslink = cfg['feeds']['rsslink']
phoneno = cfg['sms']['phoneno']
password = cfg['sms']['password']
groupname = cfg['sms']['groupname']
apiVersion = cfg['api']['version']
countryCode = cfg['api']['countrycode']

feed_item = getRss(rsslink)

storeMsg(feed_item)

token = connect.tryLogin(salt, challenge, password, phoneno, apiVersion, countryCode)

msg = message.getMsg()

message.postMsg(msg, groupname, token, apiVersion)

connect.tryLogout(token, apiVersion)
