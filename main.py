import requests
import mysql.connector

import os
STEAM_API_TOKEN = os.environ.get('STEAM_API_TOKEN')
STEAM_API_ID = os.environ.get('STEAM_API_ID')

GREPTIME_HOST = os.environ.get('GREPTIME_HOST')
GREPTIME_PORT = os.environ.get('GREPTIME_PORT')
GREPTIME_DATABASE = os.environ.get('GREPTIME_DATABASE')
GREPTIME_USERNAME = os.environ.get('GREPTIME_USERNAME')
GREPTIME_PASSWORD = os.environ.get('GREPTIME_PASSWORD')


def insert_to_db(data):
    # Establish a connection to the MySQL server
    conn = mysql.connector.connect(
        host=GREPTIME_HOST,
        port=GREPTIME_PORT,
        database=GREPTIME_DATABASE,
        user=GREPTIME_USERNAME,
        password=GREPTIME_PASSWORD
    )


    # Create a cursor object
    cursor = conn.cursor()

    # Create a table in the database
    cursor.execute('''CREATE TABLE IF NOT EXISTS "recently_play_games" (
                                                  "ts" TIMESTAMP(3) NOT NULL DEFAULT current_timestamp(),
                                                  "appid" INT NULL,
                                                  "game_name" STRING NULL,
                                                  "playtime_2weeks" FLOAT NULL,
                                                  "playtime_forever" FLOAT NULL,
                                                  TIME INDEX ("ts"))''')

    # Write an SQL query to insert data into the database
    for game in data['response']['games']:
        sql = "INSERT INTO recently_play_games (appid, game_name, playtime_2weeks, playtime_forever) VALUES (%s, %s, %s, %s)"
        val = (game['appid'], game['name'], round(game['playtime_2weeks']/60,1), round(game['playtime_forever']/60,1))

        # Execute the SQL query
        cursor.execute(sql, val)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # get recently played games
    url =f'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1?key={STEAM_API_TOKEN}&steamid={STEAM_API_ID}'

    response = requests.get(url)
    data = response.json()

    print(data)
    insert_to_db(data)








