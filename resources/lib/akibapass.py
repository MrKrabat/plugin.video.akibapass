# -*- coding: utf-8 -*-
# Akibapass - Watch videos from the german anime platform Akibapass.de on Kodi.
# Copyright (C) 2016 - 2017 MrKrabat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

    if (username == "") or (password == ""):
        # open addon settings
        args._addon.openSettings()
        return False
    else:
        # login
        success = login.login(username, password, args)
        if success == True:
            # list menue
            xbmcplugin.setContent(int(sys.argv[1]), "tvshows")
            check_mode(args)
        else:
            # login failed
            xbmc.log("[PLUGIN] %s: Login failed" % args._addonname, xbmc.LOGERROR)
            xbmcgui.Dialog().ok(args._addonname, args._addon.getLocalizedString(30040))
            return False


def check_mode(args):
    """Run mode-specific functions
    """
    try:
        mode = args.mode
    except:
        # call from other plugin
        mode = "videoplay"
        args.name = "Video"
        args.episode, args.rating, args.plot, args.year, args.studio, args.icon = ("None",) * 6

        if hasattr(args, "id"):
            args.url = "/de/v2/catalogue/episode/" + args.id
        elif hasattr(args, "url"):
            args.url = args.url[24:]
        else:
            mode = None

    if mode is None:
        showMainMenue(args)
    elif mode == "catalog":
        netapi.showCatalog(args)
    elif mode == "search":
        netapi.searchAnime(args)
    elif mode == "downloads":
        netapi.myDownloads(args)
    elif mode == "collection":
        netapi.myCollection(args)
    elif mode == "list_season":
        netapi.listSeason(args)
    elif mode == "list_episodes":
        netapi.listEpisodes(args)
    elif mode == "videoplay":
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
                  {"title": args._addon.getLocalizedString(30020),
                   "mode":   "catalog"})
    list.add_item(args,
                  {"title": args._addon.getLocalizedString(30021),
                   "mode":   "search"})
    list.add_item(args,
                  {"title": args._addon.getLocalizedString(30022),
                   "mode":   "downloads"})
    list.add_item(args,
                  {"title": args._addon.getLocalizedString(30023),
                   "mode":   "collection"})
    list.endofdirectory()
