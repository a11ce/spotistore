import spotipy
import spotipy.util as util
import sys
import config

scope = 'playlist-modify-public playlist-read-private playlist-modify-private'


def getTracks(listID):
    batch = sp.user_playlist(config.username, listID)
    tracks = batch['tracks']['items']
    if 'next' in batch['tracks']:
        batch = batch['tracks']
        # TODO what
        while batch is not None and 'next' in batch:
            batch = sp.next(batch)
            if batch is not None:
                tracks.extend(batch['items'])
    return [track['track']['uri'] for track in tracks]


def encode(data, base):
    ret = []
    while data > 0:
        ret.append(data % base)
        data = data // base
    return ret


def decode(data, base):
    ret = 0
    for v in reversed(data):
        ret += v
        ret *= base
    return ret


def init():
    global sp
    global KEY_PL
    token = util.prompt_for_user_token(config.username, scope)
    sp = spotipy.Spotify(auth=token)
    KEY_PL = getTracks(config.keyPlaylist)


def makePlaylistWithTracks(tracks, name):
    newPl = sp.user_playlist_create(config.username, name)['uri']

    for i in range(0, len(tracks), 100):
        sp.user_playlist_add_tracks(config.username, newPl, tracks[i:i + 100])
    return newPl


def writePl(b):
    enc = encode(int.from_bytes(b, "little"), 256)

    encPl = [KEY_PL[v] for v in enc]
    return makePlaylistWithTracks(encPl, "spotiStore playlist")


def readPl(uri):
    tr = getTracks(uri)
    dec = decode([KEY_PL.index(v) for v in tr], len(KEY_PL))
    return dec.to_bytes(len(tr) + 8, 'little')


def usage():
    print(
        "Usage:\n\tspotiStore.py [write | read uri]\n\tdata to stdin if writing"
    )
    exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    if config.username == "your_spotify_username_here":
        print("put your spotify username in config.py before use")
        exit(2)

    init()
    if sys.argv[1] == "write":
        print(writePl(sys.stdin.buffer.read()))
    elif sys.argv[1] == "read":
        sys.stdout.buffer.write(readPl(sys.argv[2]))
    else:
        usage()
