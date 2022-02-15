import sys
import spotipy
import spotipy.util as util
import json
import hashlib
import numpy as np

scope = 'playlist-modify-public playlist-read-private playlist-modify-private'
keyList = 'spotify:user:oxa11ce:playlist:7nokn7fgCK6PoGIi8UMJkm'
keyTracks = []
#messageText = "hello world"

def encode(inpString):
    retArr = []
    for char in inpString:
        retArr.append(ord(char) - 32)
    return retArr
def decodeArr(inpArr):
    retArr = []

    for num in inpArr:
        retArr.append(chr(num+32))
    return retArr
def decode(inpInt):
    return chr(inpInt+32)


def init():
    if len(sys.argv) > 2:
        username = sys.argv[1]
    else:
        print ("Usage: %s username [s or l]" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
            sp = spotipy.Spotify(auth=token)



    else:
        print ("Can't get token for " + username)

    keyListID = keyList.split(':')[4]

    results = sp.user_playlist(username, keyListID)
    for item in results['tracks']['items']:
            #print item['track']['uri']
        keyTracks.append(item['track']['uri'])

    return username, sp, keyTracks

def save():

    username, sp, keyTracks = init()
    messageText = input("Message: ")
    newName = "spoti-" + (hashlib.md5(messageText.encode('utf-8')).hexdigest())
    newList = sp.user_playlist_create(username, newName)
    newURI = newList['uri']
    sp.user_playlist_change_details(username, newURI.split(':')[4], public=False)
    print(newList['uri'])
    print(len(keyTracks))

    toAdd = []
    for vals in encode(messageText):
        print(str(vals) + ' '+ keyTracks[vals])
        toAdd.append(keyTracks[vals])

    sp.user_playlist_add_tracks(username, newURI, toAdd)
    print(newURI)

def load():
    username, sp, keyTracks = init()
    messageURI = input("URI:")
    downTracks = []
    results = sp.user_playlist(username, messageURI)
    for item in results['tracks']['items']:
            #print item['track']['uri']
        downTracks.append(item['track']['uri'])
    for track in downTracks:
        print(decode(keyTracks.index(track)))

def main():
    if sys.argv[2] == 's':
        save()
    elif sys.argv[2] == 'l':
        load()





if __name__ == "__main__":
    main()
