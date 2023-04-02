import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os


def get_all_episodes_with_python(sp):
    episodes = []
    offset = 0
    limit = 50  # max limit
    market='BR' 
    
    while True:
        results = sp.search(q='Python', type='episode', limit=limit, offset=offset, market=market)
        episodes += results['episodes']['items']
        offset += limit
        if len(results['episodes']['items']) == 0:
            break  
    return episodes


# Authentication 
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

auth_manager = SpotifyClientCredentials(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager = auth_manager)

# Get episodes
episodes = get_all_episodes_with_python(sp)

for i, episode in enumerate(episodes):
    print(f'{i} - {episode["name"][:100]}')
    