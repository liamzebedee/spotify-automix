import spotify
import threading
from sets import Set
import logging
# logging.basicConfig(level=logging.DEBUG)


def interact():
	import code
	code.InteractiveConsole(locals=globals()).interact()


playlist = None
USERNAME = ""
PASSWORD = ""
PLAYLIST_SPOTIFY_URI = "spotify:user:liamzebedee:playlist:1YO3OxtmY10zZcj5u8GwAC"
STARTING_ARTIST_INSPIRATION = 'Gold Panda'


config = spotify.Config()
config.user_agent = 'x'
config.tracefile = b'./libspotify-trace.log'
config.load_application_key_file()

logged_in_event = threading.Event()

def connection_state_listener(session):
	print("New conn state")
	if session.connection.state is spotify.ConnectionState.LOGGED_IN:
		logged_in_event.set()

print("Creating Spotify sesh")
session = spotify.Session(config)
session.process_events()

print("a")
loop = spotify.EventLoop(session)
loop.start()
session.on(
	spotify.SessionEvent.CONNECTION_STATE_UPDATED,
	connection_state_listener)

print("Logging in...")
session.login(USERNAME, PASSWORD, remember_me=True)
# session.relogin()

print("Waiting...")
logged_in_event.wait()

print(session.user)


def getTracks(artist):
	try:
		return artist.browse().load().tophit_tracks
	except:
		return []

def getSimilar(artist):
	return artist.browse().load().similar_artists


added_artists = Set()

def addSongsFor(artist, n):
	if n == 0:
		# print("Stopping...")
		return
	if artist in added_artists:
		# print("Artist %s already in playlist" % artists.load().name)
		return

	print("Adding songs for %s" % artist.load().name)
	added_artists.add(artist)

	tracks = getTracks(artist)
	if (len(tracks) > 0):
		playlist.add_tracks(tracks[0:4])

	for artist in getSimilar(artist):
		addSongsFor(artist, n - 1)

def getArtistByName(name):
	return session.search(name).load().artists[0]

print("Getting artist")
playlist = session.get_playlist(PLAYLIST_SPOTIFY_URI)
addSongsFor(getArtistByName(STARTING_ARTIST_INSPIRATION), 6)



