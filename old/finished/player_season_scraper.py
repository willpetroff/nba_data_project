"""
Python 3.4.3

This is a script that gets regular and post season per-game statistics for all players from NBA.com

Created: 5/27/15
"""
import urllib.request
from json import loads
import os
import time
import csv
from shutil import move
from random import randint


def player_list_gen():  # Populates id_list with player Id numbers from player_id_file
    file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\'
    file_name = 'player_id_file.csv'
    with open(file_dir+file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        id_list = [line[0] for line in reader]
    return id_list


def player_season_scraper(player):  # Scrapes player per-game statistics by season when given player id numbers
    url = 'http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID='+player
    try:
        req = urllib.request.urlopen(url)
    except urllib.request.HTTPError:  # Excepts HTTPError for non-existent player pages and creates an error list
        error_list.append(player)
    else:
        data = loads(req.read().decode())
        # unpacking json data where yearly stats are nested as lists by seasons and split between regular/post seasons
        temp_cab_reg = [item for item in data['resultSets'][0]['rowSet']]
        temp_cab_post = [item for item in data['resultSets'][2]['rowSet']]
        header_cab = [item for item in data['resultSets'][0]['headers']]  # Generates column headers for statistics
        temp_cab_reg.insert(0, header_cab)
        temp_cab_post.insert(0, header_cab)
        with open(player+'_regular_season_totals.csv', 'w', newline='') as regular_csv:  # Creates regular season file
            writer = csv.writer(regular_csv)
            writer.writerows(temp_cab_reg)
        with open(player+'_post_season_totals.csv', 'w', newline='') as post_csv:  # Creates post season file
            writer = csv.writer(post_csv)
            writer.writerows(temp_cab_post)


def file_mover(player):  # Moves player files from local folder to new folder
    file_dir_reg = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\player regular season\\'
    file_dir_post = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\player post season\\'
    file_name_reg = player+'_regular_season_totals.csv'
    file_name_post = player+'_post_season_totals.csv'
    if not os.path.exists(file_dir_reg):  # Checks to see if regular season path exists and creates it if not
        os.makedirs(file_dir_reg)
    if not os.path.exists(file_dir_post):  # Checks to see if post season path exists and creates it if not
        os.makedirs(file_dir_post)
    move(file_name_reg, file_dir_reg+file_name_reg)
    move(file_name_post, file_dir_post+file_name_post)


if __name__ == '__main__':
    error_list = []
    player_id_list = player_list_gen()
    for player_id in player_id_list:
        print(player_id)
        player_season_scraper(player_id)
        file_mover(player_id)
        time.sleep(randint(1, 5))
    print(error_list)
