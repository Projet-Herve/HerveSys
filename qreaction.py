#!/usr/bin/python
# -*- coding:utf-8 -*-

import subprocess, json , requests


def scanner_qr():

	try :
		c=subprocess.Popen(['zbarcam'], stdout=subprocess.PIPE,bufsize=256, universal_newlines=True)
		try:
			while True:
				output=c.stdout.readline()
				if output != "":
					url = ":".join(output.split(':')[1:])
					print ('Call : '+url) 
					requests.get(url)
		except KeyboardInterrupt:
			c.kill()
		return
	except:
		return "Il y a eu une erreur, il semble que zbarcam ne soit pas installé"