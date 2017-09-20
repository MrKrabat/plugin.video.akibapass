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
import xbmcaddon


_plugId = 'plugin.video.akibapass'

# plugin constants
__addon__  = xbmcaddon.Addon(id=_plugId)
__plugin__    = __addon__.getAddonInfo('name')
__version__   = __addon__.getAddonInfo('version')

xbmc.log("[PLUGIN] %s: version %s' initialized" % (__plugin__, __version__))

if __name__ == "__main__":
    from resources.lib import akiba_main
	# start addon
    akiba_main.main()

sys.modules.clear()
