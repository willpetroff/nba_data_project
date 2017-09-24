"""
This script retrieves and parses SVU box-score data from NBA.com

 Create: 10/28/15
"""

import urllib.request
import json
import os
import time
import csv
from shutil import move

def run_check(current_date):
    last_run_file = 'runtime_data.txt'
    folder_path = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\runtime data\\svu_boxscore\\'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    if last_run_file in os.listdir(folder_path):
        if


def game_day(month, day, year):
    url = 'http://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate='+str(month)+'%2F'+str(day)\
          +'%2F'+str(year)
    req = urllib.request.urlopen(url)
    data = json.loads(req.read().decode())





if __name__ == '__main__':

