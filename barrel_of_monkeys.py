#!/usr/bin/python
from xml.dom import minidom
import collections
import random

def create_song_dict(filename):
    f = open(filename)
    dom = minidom.parse(f)
    songs = dom.getElementsByTagName('Song')
    song_dict = collections.defaultdict(int)
    for song in songs:
        song_dict[song.getAttribute('name')] = song.getAttribute('duration')
    f.close()
    return song_dict

def create_playlist(start, end, songs, verify):
    def helper(song, end, playlist):
        def match(s):
            return (s.lower()[0] == song.lower()[-1]) and s not in playlist
        def possible_end(s):
            return (end.lower()[0] == s.lower()[-1]) and s not in playlist
        matching_songs = filter(match, songs.keys())
        penultimates = filter(possible_end, matching_songs)
        for penultimate in penultimates:
            if verify(playlist + [penultimate]):
                return playlist + [penultimate]
        for title in matching_songs:
            return helper(title, end, playlist + [title])
        return possible_playlist
    return helper(start, end, [])

def verify_length(num):
    def verify_playlist(playlist):
        return True if len(playlist) == num else False
    return verify_playlist

def driver():
    songs = create_song_dict('/Users/rickyghov/Downloads/SongLibrary.xml')
    print create_playlist('Fantasy Girl', 'Sexy Boy', songs, verify_length(10))
    print create_playlist('Fantasy Girl', 'Sexy Boy', songs, verify_length(1))
    
driver()
