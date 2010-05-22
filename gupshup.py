#!/usr/bin/env python

from iniparse import INIConfig
import connect
import message


cfg = INIConfig(open('settings.ini'))
phoneno = cfg['sms']['phoneno']
password = cfg['sms']['password']
apiVersion = cfg['api']['version']
countryCode = cfg['api']['countrycode']
groupname = cfg['sms']['groupname']

salt, challenge = connect.getChallenge(phoneno, password, apiVersion, countryCode)

token = connect.tryLogin(salt, challenge, password, phoneno, apiVersion, countryCode)

msg = message.getMsg()

message.postMsg(msg, groupname, token, apiVersion)

connect.tryLogout(token, apiVersion)
