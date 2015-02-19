# -*- coding: utf-8 -*-
#------------------------------------------------------------
# SuperIPTV - XBMC Add-on by Darkmantk
# Version 0.0.1 (16.09.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-2.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import xbmc
import plugintools


art = xbmc.translatePath(os.path.join('http://downloads.openspa.info/stream/icons', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.superiptv/tmp', ''))


# Entry point
def run():
    plugintools.log("---> SuperIPTV.run <---")

    # Obteniendo parámetros...
    params = plugintools.get_params()

    if params.get("action") is None:
        main_list(params)
    else:
       action = params.get("action")
       url = params.get("url")
       exec action + "(params)"

    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("SuperIPTV.main_list "+repr(params))

    data = plugintools.read("http://downloads.openspa.info/stream/streams.xml")
    matches = plugintools.find_multiple_matches(data,'<iptv>(.*?)</iptv>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        action = plugintools.find_single_match(entry,'<action>(.*?)</action>')
        genre = plugintools.find_single_match(entry,'<genre>(.*?)</genre>')
        url = plugintools.find_single_match(entry,'<uri>(.*?)</uri>')

        # Control paternal
        adults = plugintools.get_setting("adults")
        if adults == "false":
            print "Control paternal en marcha"
            if genre.find("Adultos") >= 0 :
                plugintools.log("Activando control paternal...")
            else:
                fixed = title
                plugintools.add_item( action = "play" , plot = fixed , title = fixed , thumbnail = art + "/" + thumbnail , url = url , folder = False , isPlayable = True )
        else:
            fixed = title
            plugintools.add_item( action = "play" , plot = fixed , title = fixed , thumbnail = art + "/" + thumbnail , url = url , folder = False , isPlayable = True )

def play(params):
    plugintools.log("SuperIPTV.play " + repr(params))
    plugintools.log("Playing file...")
    url = params.get("url")

    # Notificación de inicio de resolver en caso de enlace RTMP
    if url.startswith("rtmp") == True:
        msg = "Resolviendo enlace ... "
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('SuperIPTV', msg, 3 , 'icon.png'))
        plugintools.play_resolved_url( params.get("url") )
    elif url.startswith("http") == True:
            url = params.get("url")
            plugintools.play_resolved_url(url)
    elif url.startswith("rtp") >= 0:  # Control para enlaces de Movistar TV
        plugintools.play_resolved_url(url)
    else:
        plugintools.play_resolved_url(url)

def runPlugin(url):
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')

run()
