import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
import requests


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
            host='localhost',
            database='spotifydb',
            user='postgres',
            password='postgres'
        )
        return self.conn
        
    def criate_db(self, sql):
        self.conn = self.connect_db()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()
        self.conn.close()   
    
    def insert_db(self, sql):
        self.conn = self.connect_db()
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            self.conn.rollback()
            self.cur.close()
            return 1
        self.cur.close()
        
    def select_db(self, sql):
        self.conn = self.connect_db()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.recset = self.cur.fetchall()
        self.records = []
        for rec in self.recset:
            self.records.append(rec)
        self.conn.close()
        return self.records
        
        
# Authentication
sp = authentication()

# Get episodes
episodes = get_all_episodes_with_python(sp)
df = pd.DataFrame(episodes)

# Database Class
db = Database()

# Creating tables
sql = 'DROP TABLE IF EXISTS public.episodes CASCADE'
db.criate_db(sql)

sql = '''
    CREATE TABLE IF NOT EXISTS episodes (
        id VARCHAR(25) PRIMARY KEY,
        description TEXT,
        link VARCHAR(60)
)'''
db.criate_db(sql)


sql = 'DROP TABLE IF EXISTS public.images'
db.criate_db(sql)

sql = '''
    CREATE TABLE IF NOT EXISTS images (
        id_episode VARCHAR(25),
        number INTEGER,
        height INTEGER,
        width INTEGER,
        url VARCHAR(100),
        PRIMARY KEY (id_episode, number),
        FOREIGN KEY (id_episode) REFERENCES episodes(id)
            ON DELETE CASCADE
		    ON UPDATE CASCADE
)'''
db.criate_db(sql)

# Inserting data in database
for i in df.index:
    sql = f"""
        INSERT INTO episodes (id, description, link)
        VALUES ($${df['id'][i]}$$, $${df['description'][i]}$$, $${df['external_urls'][i]['spotify']}$$);
    """ 
    
    db.insert_db(sql)

for i, row in df.iterrows():
    for j, image in enumerate(row['images']):
        sql = f"""
            INSERT INTO images (id_episode, number, height, width, url)
            VALUES ($${row['id']}$$, {j+1}, {image['height']}, {image['width']}, $${image['url']}$$);
        """ 
        
        db.insert_db(sql)


# Creating folder
if not os.path.exists('images'):
    os.mkdir('images')

# Querying data
sql = 'SELECT id_episode, url FROM public.images'
images = db.select_db(sql)

# Tranformando os dados da consulta no PostegreSQL em DataFrame
df_images = pd.DataFrame(images, columns=['id', 'url'])

for i, row in df_images.iterrows():
    response = requests.get(row['url'])
    image_filename = f"{row['id']}_{i}.jpg"
    id = ''
    if id != row['id']:
        id = row['id']
        path = f'images/{id}'
        if not os.path.exists(f'{path}/'):
            os.mkdir(f'{path}/')
    image_path = os.path.join(f'images/{id}', image_filename)
    
    with open(image_path, 'wb') as f:
        f.write(response.content)
    