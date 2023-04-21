from dotenv import load_dotenv
import os
import pandas as pd
import requests

from modules.database import Database
from modules.spotify_api import Spotipy
   
   
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

HOST='localhost'
DATABASE='spotifydb'
USER='postgres'
PASSWORD='postgres'

# Authentication
spotipy = Spotipy(CLIENT_ID, CLIENT_SECRET)
sp = spotipy.authentication()

# Get episodes
episodes = spotipy.get_all_episodes_with_python(sp)
#df = pd.DataFrame(episodes)

# Database Class
db = Database(HOST, DATABASE, USER, PASSWORD)

# Creating tables
sql = 'DROP TABLE IF EXISTS public.episodes CASCADE'
db.criate_db(sql)

sql = '''
    CREATE TABLE IF NOT EXISTS episodes (
        id VARCHAR(25) PRIMARY KEY,
        description TEXT,
        link VARCHAR(60),
        link_info VARCHAR(60)
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
'''for i in df.index:
    sql = f"""
        INSERT INTO episodes (id, description, link, link_info)
        VALUES ($${df['id'][i]}$$, $${df['description'][i]}$$, $${df['external_urls'][i]['spotify']}$$, $${df['href'][i]}$$);
    """
    
    db.insert_db(sql)

for i, row in df.iterrows():
    for j, image in enumerate(row['images']):
        sql = f"""
            INSERT INTO images (id_episode, number, height, width, url)
            VALUES ($${row['id']}$$, {j+1}, {image['height']}, {image['width']}, $${image['url']}$$);
        """ 

        db.insert_db(sql)'''
        
episode = tuple()
episode_list = list()
for ep in episodes:
    episode = ep['id'], ep['description'], ep['external_urls']['spotify'], ep['href']
    episode_list.append(episode)
    
image = tuple()
image_list = list()
for ep in episodes:
    for j, im in enumerate(ep['images']):
        image = ep['id'], j+1, im['height'], im['width'], im['url']
        image_list.append(image)


sql = "INSERT INTO episodes (id, description, link, link_info) VALUES %s"
db.bulk_insert_db(sql, episode_list)

sql = "INSERT INTO images (id_episode, number, height, width, url) VALUES %s"
db.bulk_insert_db(sql, image_list)

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

