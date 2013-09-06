#!/usr/bin/env python

#-*-coding:UTF-8-*-

'''
Created on 2013-4-17
@author: yadongwen
usage: $0 [album url of xiami.com]
'''

import os
import sys
import re
import urllib
import urllib2
import math

def get_artist(html):
    m = re.search('<a href="/artist/\d+">([^<]+)<', html)
    return m.group(1)

def get_album_name(html):
    m = re.search('<h1 property="v:itemreviewed">([^<]+)<', html)
    return m.group(1)

def get_songs(html, album_name, artist):
    matches = re.findall('<a href="/song/(\d+)" title="">([^<]+)</a>', html)
    songs = []
    i = 1
    for (song_id, song_name) in matches:
        h = {'track_id' : i,
             'song_id' : song_id,
             'song_name' : song_name,
             'album_name' : album_name,
             'artist' : artist,
             'download_url' : get_song_download_url(song_id)
             }
        songs.append(h)
        i += 1
    return songs

def get_song_download_url(song_id):
    user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'name' : 'Michael Foord',
              'location' : 'Northampton',
              'language' : 'Python'
              }
    headers = {'User-Agent' : user_agent}
    data = urllib.urlencode(values)
    req = urllib2.Request('http://www.xiami.com/song/playlist/id/'
                          + str(song_id)
                          + '/object_name/collect/object_id/0', data, headers)

    response = urllib2.urlopen(req)
    html = response.read()

    m = re.search('<location>([^<]+)</location>', html)
    code = m.group(1)

    return decode_location(code)

def decode_location(code):
    l10 = None
    l2 = int(code[0])
    l3 = code[1:]
    l4 = int(math.floor(len(l3)/l2))
    l5 = len(l3) % l2
    l6 = []
    l7 = 0
    while(l7 <l5):
        if l7 >= len(l6):
            l6.append('')
        l6[l7] = l3[(l4+1)*l7:(l4+1+(l4+1)*l7)]
        l7+=1
    l7=l5
    while l7<l2:
        if l7>=len(l6):
            l6.append(l3[(l4*(l7-l5)+(l4+1)*l5):(l4+(l4*(l7-l5)+(l4+1)*l5))])
        else:
            l6[l7] = l3[(l4*(l7-l5)+(l4+1)*l5):(l4+(l4*(l7-l5)+(l4+1)*l5))]
        l7+=1
    l8=''
    l7=0
    while l7<len(l6[0]):
        l10=0
        while l10<len(l6):
            if l7 < len(l6[l10]):
                l8 = l8 + l6[l10][l7]
            l10+=1
        l7+=1
    l8=urllib.unquote(l8)
    l9=''
    l7=0
    while l7<len(l8):
        if l8[l7]=='^':
            l9+='0'
        else:
            l9+=l8[l7]
        l7+=1
    l9=l9.replace('+', ' ')
    return l9


def get_album_download_info(url):
    user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'name' : 'Mic',
              'location' : 'Northa',
              'language' : 'Pyt'
              }
    headers = {'User-Agent' : user_agent}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data, headers)

    response = urllib2.urlopen(req)
    html = response.read()

    artist = get_artist(html)
    album_name = get_album_name(html)
    songs = get_songs(html, album_name, artist)

    return {'artist' : artist,
            'album_name' : album_name,
            'songs' : songs
            }

if __name__ == '__main__':
    album = get_album_download_info(sys.argv[1])
    #print album

    print album['artist'] + ' - ' + album['album_name']

    try:
        if not os.path.exists('music'):
            os.mkdir('music')
        os.chdir('music')
        if not os.path.exists(album['artist']):
            os.mkdir(album['artist'])
        os.chdir(album['artist'])
        if os.path.exists(album['album_name']):
            print 'Album ' + album['album_name'] + ' already exists. Remove it to download again.'
            sys.exit(-1)
        os.mkdir(album['album_name'])
        os.chdir(album['album_name'])
        for song in album['songs']:
            if song['track_id']<10:
                mp3_filename = '0' + str(song['track_id']) + '. ' + song['song_name'] + '.mp3'
            else:
                mp3_filename = str(song['track_id']) + '. ' + song['song_name'] + '.mp3'

            mp3_filename = mp3_filename.replace('?', '')
            mp3_filename = mp3_filename.replace(':', '')
            mp3_filename = mp3_filename.replace('<', '')
            mp3_filename = mp3_filename.replace('>', '')
            mp3_filename = mp3_filename.replace('/', '')
            mp3_filename = mp3_filename.replace('\\', '')
            mp3_filename = mp3_filename.replace('!', '')
            mp3_filename = mp3_filename.replace('*', '')
            mp3_filename = mp3_filename.replace('|', '')
            mp3_filename = mp3_filename.replace('\'', '')
            print mp3_filename + ' - ' + song['download_url'] + '...downloading'

            urllib.urlretrieve(song['download_url'], mp3_filename)

        os.chdir('..')
        os.chdir('..')
        os.chdir('..')
    except Exception, e:
        print e
