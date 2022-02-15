# spotiStore

> Store data in Spotify playlists

## Setup

- `git clone git@github.com:a11ce/spotistore.git`
- `python3 -m pip install spotipy` if you don't have it
- Edit `config.py`: Add your Spotify username, (and optionally your own key playlist, but you can also just use mine.)

## Usage

- Run `python3 spotiStore.py write` and send data to stdin. It reads until EOF then uploads the data to a playlist and prints the URI.
- Run `python3 spotiStore read [playlist URI]` to read back the data. Be sure the `keyPlaylist` in `config.py` matches the one used to write a given playlist.

## Example

```
$ python3 spotiStore.py write < udhr_eo.txt
spotify:playlist:2ftPyBrRvhvVWC7hkwyvSJ
$ python3 spotiStore.py read spotify:playlist:2ftPyBrRvhvVWC7hkwyvSJ
Ĉiuj homoj estas denaske liberaj kaj egalaj laŭ digno kaj rajtoj. Ili posedas racion kaj konsciencon, kaj devus konduti unu al alia en spirito de frateco.
```

--- 

All contributions are welcome by pull request or issue.

spotiStore is licensed under GNU General Public License v3.0. See [LICENSE](../master/LICENSE) for full text.
