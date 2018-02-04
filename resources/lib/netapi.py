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

import re
import sys
from bs4 import BeautifulSoup
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import xbmc
import xbmcgui
import xbmcplugin

from . import login
from . import view


def showCatalog(args):
    """Show all animes
    """
    xbmc.log("DEBUG POINT #2", xbmc.LOGERROR)
    response = urlopen("https://www.akibapass.de/de/v2/catalogue")
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find("ul", {"class": "catalog_list"})

    for li in ul.find_all("li"):
        plot  = li.find("p", {"class": "tooltip_text"})
        stars = li.find("div", {"class": "stars"})
        star  = stars.find_all("span", {"class": "-no"})
        thumb = li.img["src"].replace(" ", "%20")
        if thumb[:4] != "http":
            thumb = "https:" + thumb

        view.add_item(args,
                      {"url":         li.a["href"],
                       "title":       li.find("div", {"class": "slider_item_description"}).span.strong.string.strip(),
                       "tvshowtitle": li.find("div", {"class": "slider_item_description"}).span.strong.string.strip(),
                       "mode":        "list_season",
                       "thumb":       thumb,
                       "fanart":      thumb,
                       "rating":      str(10 - len(star) * 2),
                       "plot":        plot.contents[3].string.strip(),
                       "year":        li.time.string.strip()},
                      isFolder=True, mediatype="video")

    view.endofdirectory()


def listLastEpisodes(args):
    """Show last aired episodes
    """
    response = urlopen("https://www.akibapass.de/de/v2")
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find_all("ul", {"class": "js-slider-list"})
    if not ul:
        view.endofdirectory()
        return

    for li in ul[1].find_all("li"):
        thumb = li.img["src"].replace(" ", "%20")
        if thumb[:4] != "http":
            thumb = "https:" + thumb

        view.add_item(args,
                      {"url":    li.a["href"],
                       "title":  li.img["alt"],
                       "mode":   "videoplay",
                       "thumb":  thumb,
                       "fanart": thumb,
                       "plot":   li.find("a", {"class": "slider_item_season"}).string.strip()},
                      isFolder=False, mediatype="video")

    view.endofdirectory()


def listLastSimulcasts(args):
    """Show last simulcasts
    """
    response = urlopen("https://www.akibapass.de/de/v2")
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find_all("ul", {"class": "js-slider-list"})
    if not ul:
        view.endofdirectory()
        return

    for li in ul[2].find_all("li"):
        plot  = li.find("p", {"class": "tooltip_text"})
        stars = li.find("div", {"class": "stars"})
        star  = stars.find_all("span", {"class": "-no"})
        thumb = li.img["src"].replace(" ", "%20")
        if thumb[:4] != "http":
            thumb = "https:" + thumb

        view.add_item(args,
                      {"url":         li.a["href"],
                       "title":       li.find("div", {"class": "slider_item_description"}).span.strong.string.strip(),
                       "tvshowtitle": li.find("div", {"class": "slider_item_description"}).span.strong.string.strip(),
                       "mode":        "list_season",
                       "thumb":       thumb,
                       "fanart":      thumb,
                       "rating":      str(10 - len(star) * 2),
                       "plot":        plot.contents[-1].string.strip(),
                       "year":        li.time.string.strip()},
                      isFolder=True, mediatype="video")

    view.endofdirectory()


def searchAnime(args):
    """Search for animes
    """
    d = xbmcgui.Dialog().input(args._addon.getLocalizedString(30021), type=xbmcgui.INPUT_ALPHANUM)
    if not d:
        return

    post_data = urlencode({"search": d})
    response = urlopen("https://www.akibapass.de/de/v2/catalogue/search", post_data.encode("utf-8"))
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find("ul", {"class": "catalog_list"})
    if not ul:
        view.endofdirectory()
        return

    for li in ul.find_all("li"):
        plot  = li.find("p", {"class": "tooltip_text"})
        stars = li.find("div", {"class": "stars"})
        star  = stars.find_all("span", {"class": "-no"})
        thumb = li.img["src"].replace(" ", "%20")
        if thumb[:4] != "http":
            thumb = "https:" + thumb

        view.add_item(args,
                      {"url":    li.a["href"],
                       "title":  li.find("div", {"class": "slider_item_description"}).span.strong.string.strip(),
                       "mode":   "list_season",
                       "thumb":  thumb,
                       "fanart": thumb,
                       "rating": str(10 - len(star) * 2),
                       "plot":   plot.contents[3].string.strip(),
                       "year":   li.time.string.strip()},
                      isFolder=True, mediatype="video")

    view.endofdirectory()


def myDownloads(args):
    """View download able animes
    May not every episode is download able.
    """
    response = urlopen("https://www.akibapass.de/de/v2/mydownloads")
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", {"class": "big-item-list"})
    if not container:
        view.endofdirectory()
        return

    for div in container.find_all("div", {"class": "big-item-list_item"}):
        thumb = div.img["src"].replace(" ", "%20")
        if thumb[:4] != "http":
            thumb = "https:" + thumb

        view.add_item(args,
                      {"url":    div.a["href"].replace("mydownloads/detail", "catalogue/show"),
                       "title":  div.find("h3", {"class": "big-item_title"}).string.strip(),
                       "mode":   "list_season",
                       "thumb":  thumb,
                       "fanart": thumb},
                      isFolder=True, mediatype="video")

    view.endofdirectory()


def myCollection(args):
    """View collection
    """
    response = urlopen("https://www.akibapass.de/de/v2/collection")
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", {"class": "big-item-list"})
    if not container:
        view.endofdirectory()
        return

    for div in container.find_all("div", {"class": "big-item-list_item"}):
        thumb = div.img["src"].replace(" ", "%20")
        if thumb[:4] != "http":
            thumb = "https:" + thumb

        view.add_item(args,
                      {"url":    div.a["href"].replace("collection/detail", "catalogue/show"),
                       "title":  div.find("h3", {"class": "big-item_title"}).string.strip(),
                       "mode":   "list_season",
                       "thumb":  thumb,
                       "fanart": thumb},
                      isFolder=True, mediatype="video")

    view.endofdirectory()


def listSeason(args):
    """Show all seasons/arcs of an anime
    """
    response = urlopen("https://www.akibapass.de" + args.url)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    date = soup.find_all("span", {"class": "border-list_text"})[0].find_all("span")
    year = date[2].string.strip()
    date = year + "-" + date[1].string.strip() + "-" + date[0].string.strip()
    originaltitle = soup.find_all("span", {"class": "border-list_text"})[1].string.strip()
    studio = soup.find_all("span", {"class": "border-list_text"})[2].string.strip()
    plot = soup.find("div", {"class": "serie_description"}).get_text().strip()
    credits = soup.find("div", {"class": "serie_description_more"})
    credits = credits.p.get_text().strip() if credits else ""
    try:
        trailer = soup.find("span", {"class": "js-video-open"})["data-video"]
        trailer = "plugin://plugin.video.youtube/play/?video_id=" + trailer
        view.add_item(args,
                      {"url":    trailer,
                       "mode":   "trailer",
                       "thumb":  args.thumb.replace(" ", "%20"),
                       "fanart": args.fanart.replace(" ", "%20"),
                       "title":  args._addon.getLocalizedString(30024)},
                      isFolder=False, mediatype="video")
    except TypeError:
        trailer = ""

    for section in soup.find_all("h2", {"class": "slider-section_title"}):
        if not section.span:
            continue
        title = section.get_text()[6:].strip()

        view.add_item(args,
                      {"url":           args.url,
                       "title":         title,
                       "mode":          "list_episodes",
                       "thumb":         args.thumb.replace(" ", "%20"),
                       "fanart":        args.fanart.replace(" ", "%20"),
                       "season":        title,
                       "plot":          plot,
                       "plotoutline":   getattr(args, "plot", ""),
                       "studio":        studio,
                       "year":          year,
                       "premiered":     date,
                       "trailer":       trailer,
                       "originaltitle": originaltitle,
                       "credits":       credits},
                      isFolder=True, mediatype="video")

    view.endofdirectory()


def listEpisodes(args):
    """Show all episodes of an season/arc
    """
    response = urlopen("https://www.akibapass.de" + args.url)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    for season in soup.findAll(text=args.title):
        parent = season.find_parent("li")
        if not parent:
            continue

        thumb = parent.img["src"].replace(" ", "%20")
        if thumb[:4] != "http":
            thumb = "https:" + thumb

        view.add_item(args,
                      {"url":    parent.a["href"],
                       "title":  parent.img["alt"],
                       "mode":   "videoplay",
                       "thumb":  thumb.replace(" ", "%20"),
                       "fanart": args.fanart.replace(" ", "%20")},
                      isFolder=False, mediatype="video")

    view.endofdirectory()


def startplayback(args):
    """Plays a video
    """
    response = urlopen("https://www.akibapass.de" + args.url)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")

    # check if not premium
    if "Dieses Video ist nur f&#252;r Nutzer eines Abos verf&#252;gbar" in html:
        xbmc.log("[PLUGIN] %s: You need to own this video or be a premium member '%s'" % (args._addonname, args.url), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(args._addonname, args._addon.getLocalizedString(30043))
        return

    # check if we have to reactivate video
    if "reactivate" in html:
        # reactivate video
        a = soup.find("div", {"id": "jwplayer-container"}).a["href"]
        response = urlopen("https://www.akibapass.de" + a)
        html = response.read().decode("utf-8")

        # reload page
        response = urlopen("https://www.akibapass.de" + args.url)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        # check if successfull
        if "reactivate" in html:
            xbmc.log("[PLUGIN] %s: Reactivation failed '%s'" % (args._addonname, args.url), xbmc.LOGERROR)
            xbmcgui.Dialog().ok(args._addonname, args._addon.getLocalizedString(30042))
            return

    # using stream with hls+aes
    if "Klicke hier, um den Flash-Player zu benutzen" in html:
        # get stream file
        regex = r"file: \"(.*?)\","
        matches = re.search(regex, html).group(1)

        if matches:
            # manifest url
            url = "https://www.akibapass.de" + matches

            # play stream
            item = xbmcgui.ListItem(getattr(args, "title", "Title not provided"), path=url + login.getCookie(args))
            item.setMimeType("application/vnd.apple.mpegurl")
            item.setContentLookup(False)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        else:
            xbmc.log("[PLUGIN] %s: Failed to play stream" % args._addonname, xbmc.LOGERROR)
            xbmcgui.Dialog().ok(args._addonname, args._addon.getLocalizedString(30044))

    else:
        xbmc.log("[PLUGIN] %s: You need to own this video or be a premium member '%s'" % (args._addonname, args.url), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(args._addonname, args._addon.getLocalizedString(30043))
