# Whisper

### Requirements
Requires Python3.7

<<<<<<< HEAD
=======
Requires beets library because that's how it queries for music. 

>>>>>>> 009e901d6e15e888f534f3bb65c783699712d0ff
### Installation
1. Clone the repository
2. Create a virtualenv that has Python3.7
3. `pip install -r req.txt`
4. `cp config.yml.example config.yml`
5. Set up config.yml - refer to configuration section
6. `env CONFIG_LOCATION=/absolute/path/to/config.yml python src/main.py`

### Configuration
```yml
<<<<<<< HEAD
# this is where mp3 files are 
=======
# this is where mp3 files are
>>>>>>> 009e901d6e15e888f534f3bb65c783699712d0ff
music_path: "/mnt/playable_music"
# this is what plays by default
default_query: 'alphataurus'
# path to beets database file
music_db_path: '/beet/beets_data/musiclibrary.db'
# change this if you have perfomance issues
bitrate: 4096
# this is not currently implemented, but you still need to provide a valid path lol
static_playlists_path: '/var/music_man/static_playlists'
# required to connect to icecast server
ice:
<<<<<<< HEAD
  host: localhost
    port: 8000
      password: secret_password
        user: 'source'
```
=======
    host: localhost
    port: 8000
    password: secret_password
    user: 'source'
```

>>>>>>> 009e901d6e15e888f534f3bb65c783699712d0ff
