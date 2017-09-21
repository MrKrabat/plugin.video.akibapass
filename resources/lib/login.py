# -*- coding: utf-8 -*-
"""
    Akibapass.de
    Copyright (C) 2016 - 2017 MrKrabat
    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation; either version 2 of the License.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with this program
"""
import os
import cookielib
import urllib
import urllib2

import xbmc


def login(username, password, args):
	"""Login and session handler
	"""
	login_url = 'https://www.akibapass.de/de/v2/account/login?ReturnUrl=%2Fde%2Fv2'

	# create cookie path
	cookiepath = os.path.join(
		xbmc.translatePath(args._addon.getAddonInfo('profile')).decode('utf-8'),
		'cookies.lwp')

	#create cookiejar
	cj = cookielib.LWPCookieJar()
	args._cj = cj

	#lets urllib2 handle cookies
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)

	#check if session exists
	try:
		cj.load(cookiepath, ignore_discard=True)

		#check if session is valid
		response = urllib2.urlopen('https://www.akibapass.de/de/v2/catalogue')
		html = response.read()

		if 'Meine pers&#246;nlichen Informationen bearbeiten' in html:
			#session is valid
			return True

	except IOError:
		#cookie file does not exist
		pass

	#build POST data
	post_data = urllib.urlencode({'username': username,
									'password': password,
									'remember': '1',
									})

	#POST to login page
	response = urllib2.urlopen(login_url, post_data)

	#check for login string
	html = response.read()

	if 'Meine pers&#246;nlichen Informationen bearbeiten' in html:
		#save session to disk
		cj.save(cookiepath, ignore_discard=True)
		return True
	else:
		return False


def getCookie(args):
	"""Returns all cookies as string and urlencoded
	"""
	# create cookie path
	cookiepath = os.path.join(
		xbmc.translatePath(args._addon.getAddonInfo('profile')).decode('utf-8'),
		'cookies.lwp')
	#save session to disk
	args._cj.save(cookiepath, ignore_discard=True)
	
	ret = ""
	for cookie in args._cj:
		ret += urllib.urlencode({cookie.name : cookie.value}) + ";"

	return "|Cookie=" + ret[:-1]
