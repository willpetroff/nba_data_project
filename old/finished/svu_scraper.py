"""
This script grabs the various SVU player-data types and converts it to a csv file.

Edited: 4/10/16
* Updated SVU data type names
"""

from urllib.request import urlopen
import csv
from json import loads
from shutil import move
from time import sleep
import urllib.error
from random import randint
                

def primary_grab(stat_id, season_id):
    url = "http://stats.nba.com/stats/leaguedashptstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&Height=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PerMode=PerGame&PlayerExperience=&PlayerOrTeam=Player&PlayerPosition=&PtMeasureType="+stat_id+"&Season="+season_id+"&SeasonSegment=&SeasonType=Regular+Season&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight="
    # print(url)
    try_counter = 0
    while try_counter < 3:
        print(try_counter)
        try:
            target_url = urlopen(url).read()
            data = loads(target_url.decode(encoding='UTF-8'))
            with open(season_id+stat_id+'.csv', 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                header_cab = [data['resultSets'][0]['headers']]  # Grabs header row
                temp_cab = [item for item in data['resultSets'][0]['rowSet']]
                temp_cab.insert(0, header_cab[0])  # Inserts header row in front
                writer.writerows(temp_cab)
                break
        except urllib.error.HTTPError as error:
            print(error.code)
            try_counter += 1
            sleep(randint(10, 15))
    if try_counter == 3:
        return 0


def main():
    stat_name = ['SpeedDistance', 'Rebounding', 'Possessions', 'CatchShoot', 'PullUpShot', 'Defense',
                 'Drives', 'Passing', 'ElbowTouch', 'PostTouch', 'PaintTouch',
                 'Efficiency']  # SVU data type names as of 2015-16 season
    season_name = ['2015-16', '2014-15', '2013-14']  # SVU data only goes back to the 2013-14 season
    svu_data_move_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\svu data\\'
    for season in season_name:
        for stat in stat_name:
            print(stat, season)
            error_check = primary_grab(stat, season)
            # Moves csv file from local folder to data folder
            if error_check != 0:
                move(season+stat+'.csv', svu_data_move_dir+season+stat+'.csv')
            sleep(1)


if __name__ == '__main__':
    main()
