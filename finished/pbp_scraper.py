"""
Python 3.4.3

This script grabs play-by-play data for all regular season games from 1996-97 season to present from NBA.com

Created: 5/18/15
Edited: 10/21/15
*Fixed formatting errors
Edited: 11/10/15
* Set initial query to go back to 1976 for box-score data
"""
import urllib.request
from json import loads
import os
import time
import csv
from shutil import move
from random import randint


def name_pop(year):  # Populates seasons and games id lists up to a given year
    season_count = 1976  # The 1976-77 season is the first NBA season after the NBA-ABA merger.
    # The game id value is "002xx(last two numbers from first year of season)xxxxx(the game number plus needed "0"s)
    for number in range(1, 1231):  # With the current number of 15 teams, 1230 is the max number of games in a season
        game_string = '00000'[:-len(str(number))]+str(number)
        games.append(game_string)
    while season_count < year:
        seasons.append(str(season_count)[2:4])
        season_count += 1


def pbp_scraper(season, game):  # Grabs pbp data from NBA.com given season id and game id values
    url = 'http://stats.nba.com/stats/playbyplayv2?EndPeriod=10&EndRange=55800&GameID=002' + season + game +\
        '&RangeType=2&Season=2012-13&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
    file_title = season+"_"+game+"_firstpass.csv"
    with open(file_title, 'w', newline='') as text_file:
        try:
            req = urllib.request.urlopen(url)
        except urllib.request.HTTPError:  # Excepts HTTPError for non-existent games
            # Creates writer and temp_cab to create an empty file
            writer = csv.writer(text_file)
            temp_cab = []
            pass
        else:
            data = loads(req.read().decode())  # Loads and decodes JSON string with play-by-play data
            writer = csv.writer(text_file)
            header_cab = [data['resultSets'][0]['headers']]
            temp_cab = [item for item in data['resultSets'][0]['rowSet']]
            temp_cab.insert(0, header_cab[0])
        writer.writerows(temp_cab)
        dynamic_pause_1 = randint(1, 3)
        dynamic_pause_2 = randint(1, 2)
        time.sleep(dynamic_pause_1+dynamic_pause_2)  # Pause
        print((dynamic_pause_1+dynamic_pause_2), season, game)  # Shows progress
    pbp_cleaner(file_title)


def box_score_scraper(season, game):  # Grabs corresponding box-score data from NBA.com
    url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=28800&GameID=002' + season + game +\
        '&RangeType=2&Season=2011-12&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
    with open(season+'_'+game+'_boxscore.csv', 'w', newline='')as csv_file:
        try:
            req = urllib.request.urlopen(url)
        except urllib.request.HTTPError:  # Does not create empty box-score files
            pass
        else:
            data = loads(req.read().decode())
            temp_cab = [item for item in data['resultSets'][0]['rowSet']]
            writer = csv.writer(csv_file)
            writer.writerows(temp_cab)
            

def file_mover(season, game):  # Moves newly scraped files to final folder dir
    file_start = season+'_'+game
    boxscore_file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\pbp scraper\\box score\\'
    pbp_file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\pbp scraper\\pbp\\'
    if not os.path.exists(boxscore_file_dir):  # Checks for box-score path and makes it if it isn't there
        os.makedirs(boxscore_file_dir)
    if not os.path.exists(pbp_file_dir):  # Checks for play-by-play path and makes it if it isn't there
        os.makedirs(pbp_file_dir)
    move(file_start+'_boxscore.csv', boxscore_file_dir+file_start+'_boxscore.csv')
    file_name = file_start+'_secondpass.csv'
    os.remove(file_start+'_firstpass.csv')  # Removes uncleaned, unformatted play-by-play file
    move(file_name, pbp_file_dir+file_name)  # Moves cleaned and formatted play_by_play file


def pbp_cleaner(file):  # Makes initial run to clean and format play-by-play data
    temp_cab = []
    with open(file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header_flag = 0
        home_score = 0
        vis_score = 0
        score_margin = 0  # Displayed as home-team score margin (i.e. negative values when home-team is losing)
        for line in reader:
            if header_flag == 0:  # Writes new header row
                new_line = [item for item in line[:10]]
                new_line.append('HOMESCORE')
                new_line.append('VISITORSCORE')
                for item in line[11:]:
                    new_line.append(item)
                temp_cab.append(new_line)
                header_flag += 1  # Changes header_flag value after first run to pass header section
            else:
                new_line = [item for item in line[0:10]]
                score = line[10].split()  # Splits score format '100-98' to ['vis score', '-', 'home score']
                if score:  # Checks to see if score string exists
                    home_score = score[2]  # Sets/refreshes home_score value
                    vis_score = score[0]  # Sets/refreshes vis_score value
                    score_margin = str(int(home_score)-int(vis_score))  # Sets/refreshes home-team score margin
                else:
                    score = [vis_score, '', home_score]  # Sets score value to existing values
                new_line.append(score[2])
                new_line.append(score[0])
                new_line.append(score_margin)
                for item in line[12:]:
                    new_line.append(item)
                temp_cab.append(new_line)
    new_text_file = file[:8]+'_secondpass.csv'
    with open(new_text_file, 'w', newline='') as new_csv:  # Writes cleaned and formatted play-by-play rows to new file
        writer = csv.writer(new_csv)
        writer.writerows(temp_cab)

if __name__ == '__main__':
    games = []
    seasons = []
    name_pop(time.localtime()[0])
    for season_id in seasons:
        for game_id in games:
            if int(season_id) > 95:  # The 1996-97 season is the first season with play-by-play data on NBA.com
                pbp_scraper(season_id, game_id)
            box_score_scraper(season_id, game_id)
            file_mover(season_id, game_id)
