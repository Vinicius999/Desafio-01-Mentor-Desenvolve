import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

class Spotipy():
    def __init__ (self, CLIENT_ID, CLIENT_SECRET):
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
    
    def authentication(self):
        auth_manager = SpotifyClientCredentials(
            client_id = self.CLIENT_ID,
            client_secret = self.CLIENT_SECRET
        )

        self.sp = spotipy.Spotify(auth_manager = auth_manager)
        return self.sp

    def get_all_episodes_with_python(self, sp):
        self.episodes = []
        self.offset = 0
        self.limit = 50  # max limit
        self.market='BR' 
        
        while True:
            self.results = sp.search(q='Python', type='episode', limit=self.limit, offset=self.offset, market=self.market)
            self.episodes += self.results['episodes']['items']
            self.offset += self.limit
            if len(self.results['episodes']['items']) == 0:
                break  
        return self.episodes
    
    
if __name__ == "__main__":
    load_dotenv()
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    sp = Spotipy(CLIENT_ID, CLIENT_SECRET)