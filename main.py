import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os


# Authentication 
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

auth_manager = SpotifyClientCredentials(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager = auth_manager)

# First test  
results = sp.search(q='weezer', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])
    