import json
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    print("Connected to the database successfully.")
except psycopg2.Error as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

cursor = conn.cursor()

# Create table for normalized data
cursor.execute("""
CREATE TABLE IF NOT EXISTS songs (
    id VARCHAR PRIMARY KEY,
    title VARCHAR,
    danceability FLOAT,
    energy FLOAT,
    key INT,
    loudness FLOAT,
    mode INT,
    acousticness FLOAT,
    instrumentalness DOUBLE PRECISION,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    duration_ms INT,
    time_signature INT,
    num_bars INT,
    num_sections INT,
    num_segments INT,
    classes INT,
    star_rating INT DEFAULT 0
)
""")

# Load JSON data from file
with open('playlist.json', 'r') as f:
    data = json.load(f)

# Prepare data for bulk insert
songs_data = []
for i in data['id']:
    songs_data.append((
        data['id'][i],
        data['title'].get(i, ''),
        data['danceability'].get(i, 0.0),
        data['energy'].get(i, 0.0),
        data['key'].get(i, 0),
        data['loudness'].get(i, 0.0),
        data['mode'].get(i, 0),
        data['acousticness'].get(i, 0.0),
        data['instrumentalness'].get(i, 0.0),
        data['liveness'].get(i, 0.0),
        data['valence'].get(i, 0.0),
        data['tempo'].get(i, 0.0),
        data['duration_ms'].get(i, 0),
        data['time_signature'].get(i, 0),
        data['num_bars'].get(i, 0),
        data['num_sections'].get(i, 0),
        data['num_segments'].get(i, 0),
        data['classes'].get(i, "")
    ))

# Bulk insert into the table
try:
    psycopg2.extras.execute_values(cursor, """
    INSERT INTO songs (id, title, danceability, energy, key, loudness, mode, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature, num_bars, num_sections, num_segments, classes)
    VALUES %s
    ON CONFLICT (id) DO NOTHING
    """, songs_data)

    # Commit the transaction
    conn.commit()
    print('Data inserted successfully in database')
except psycopg2.Error as e:
    conn.rollback()
    print(f"Error inserting data: {e}")
finally:
    # Close the connection
    cursor.close()
    conn.close()

