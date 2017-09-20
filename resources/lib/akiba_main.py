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
import sys

import xbmc
import xbmcgui
import xbmcplugin

import cmdargs
import login
import netapi
import list


def main():
	"""Main function for the addon
	"""
	args = cmdargs.parse_args()

	# check if account is set
	username = args._addon.getSetting("akiba_username")
	password = args._addon.getSetting("akiba_password")

	if username == "" or password == "":
		# open addon settings
		args._addon.openSettings()
		return False
	else:
		# login
		success = login.login(username, password, args)
		if success==True:
			# list menue
			xbmcplugin.setContent(int(sys.argv[1]), 'movies')
			check_mode(args)
		else:
			# login failed
			xbmc.log("[PLUGIN] %s: Login failed" % args._addonname, xbmc.LOGERROR)
			xbmcgui.Dialog().ok(args._addonname, args._addon.getLocalizedString(30040))
			return False


def check_mode(args):
	"""Run mode-specific functions
	"""
	mode = args.mode

	if mode is None:
		showMainMenue(args)
	elif mode == 'catalog':
		netapi.showCatalog(args)
	elif mode == 'search':
		netapi.searchAnime(args)
	elif mode == 'downloads':
		netapi.myDownloads(args)
	elif mode == 'collection':
		netapi.myCollection(args)
	elif mode == 'list_season':
		netapi.listSeason(args)
	elif mode == 'list_episodes':
		netapi.listEpisodes(args)
	elif mode == 'videoplay':
		netapi.startplayback(args)
	else:
		# unkown mode
		xbmc.log("[PLUGIN] %s: Failed in check_mode '%s'" % (args._addonname, str(mode)), xbmc.LOGERROR)
		xbmcgui.Dialog().notification(args._addonname, args._addon.getLocalizedString(30041), xbmcgui.NOTIFICATION_ERROR)
		showMainMenue(args)


def showMainMenue(args):
	"""Show main menu
	"""
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30020),
			'mode':		'catalog'})
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30021),
			'mode':		'search'})
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30022),
			'mode':		'downloads'})
	list.add_item(args,
			{'title':	args._addon.getLocalizedString(30023),
			'mode':		'collection'})
	list.endofdirectory()

