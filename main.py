import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import psycopg2


def authentication():
    load_dotenv()

    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')

    auth_manager = SpotifyClientCredentials(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET
    )

    sp = spotipy.Spotify(auth_manager = auth_manager)
    return sp


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

class Database:
    def __init__ (self):
        print('Connecting to spotifydb...')
        
    def connect_db(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="spotifydb",
            user="postgres",
            password="postgres"
        )
        return self.conn
        
        
    def criate_db(self, sql):
        self.conn = self.connect_db()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        self.conn.close()   
    
   
# Authentication
sp = authentication()

# Get episodes
episodes = get_all_episodes_with_python(sp)

#for i, episode in enumerate(episodes):
#    print(f'{i} - {episode["name"][:100]}')

db = Database()

sql = 'DROP TABLE IF EXISTS public.episodes'
db.criate_db(sql)

sql = '''
    CREATE TABLE IF NOT EXISTS episodes (
        id VARCHAR(50) PRIMARY KEY,
        description TEXT,
        link VARCHAR(255),
        images VARCHAR(255)
    )'''
db.criate_db(sql)
