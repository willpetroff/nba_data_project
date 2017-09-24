"""
This is a script that gets the json file that contains all NBA players and their ID numbers from nba.com and edits it
into a manageable format.

Python 3.4.3

Created: 5/20/14
Edited: 6/20/16
"""
from urllib.request import urlopen
import urllib.error
from json import loads
import csv
from shutil import move
from time import sleep
from random import randint
import os
from time import localtime


def file_dir_check(directory):
    if not os.path.exists(directory):  # Checks for error path and makes it if it isn't there
        os.makedirs(directory)


def player_list_grabber(year1=localtime()[0], year2=localtime()[0]+1):
    """
    Writes master file of basic information (Name, PlayerID, Active/Inactive etc.) for all NBA players up to current
    season.
    :param year1: A given year (int). Default set to current year.
    :param year2: Must be 'year1 + 1'
    """
    season_id = str(year1)+'-'+str(year2)[2:]
    url = 'http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season=' + season_id
    flag = False
    counter = 5
    while flag is False and counter != 0:
        try:
            req = urlopen(url)
            data = loads(req.read().decode())
            flag = True
        except urllib.error.HTTPError as error_code:
            pwd = 'C:\\Users\\willp\\Documents\\projects\\nba_data_project'  # Get more pwd more generally
            error_file_dir = pwd + '\\error'
            file_dir_check(error_file_dir)
            with open(error_file_dir + '\\error_file_log.txt', 'r', newline='') as error_log:
                error_log.write(error_code)
            counter -= 1
        else:
            header_cab = [data['resultSets'][0]['headers']]  # Sets aside header values from nba json file
            temp_cab = [item for item in data['resultSets'][0]['rowSet']]  # Builds player list
            temp_cab.insert(0, header_cab[0])
            file_dir = 'C:\\Users\\willp\\Documents\\projects\\nba_data_project\\data'  # See line 43
            file_dir_check(file_dir)
            with open(file_dir + '\\player_id_file.csv', 'w', newline='') as id_file:
                writer = csv.writer(id_file)
                writer.writerows(temp_cab)


def player_entry_gen(player_id_num, name_string, player_code, height, weight,
                     player_active, approx_pos, start_year, end_year, year, month, day):  # Creates player_dict entry
    name_split = name_string.split(',')  # Splits player name from "last. first" to [last, first]
    if len(name_split) > 1:  # Nene check
        last_name = name_split[0]
        first_name = name_split[1].strip()
    else:
        first_name = name_split[0]
        last_name = ''
    # Creates and begins filling player dictionary file with player_id number as key
    player_dict[player_id_num] = {'first_name': first_name, 'last_name': last_name, 'player_code': player_code,
                                  'height': height, 'weight': weight, 'player_active': player_active,
                                  'approx_pos': approx_pos, 'start_year': start_year, 'end_year': end_year,
                                  'DOB': {'year': year, 'month': month, 'day': day}}


def player_list_gen():  # This function retrieves player id file and generates a list of players and ids.
    # Check to see if player_vitals file exists
    phys_data = 'C:\\Users\\willp\\Documents\\projects\\nba\\data\\physical data'  # See line 43
    file_dir_check(phys_data)
    if 'player_vitals.csv' in os.listdir(phys_data):
        with open(phys_data + '\\player_vitals.csv', 'r')\
                as player_vital_file:
            reader = csv.reader(player_vital_file)
            next(reader)
            for line in reader:  # Generates player_dict entries for existing players
                player_entry_gen(line[0], line[1], line[8], line[3], line[4], line[5], line[2], line[6], line[7],
                                 line[9], line[10], line[11])
    with open('C:\\Users\\willp\\Documents\\projects\\nba_data_project\\data\\player_id_file.csv', 'r') as id_file:
        reader = csv.reader(id_file)
        next(reader)
        for line in reader:
            if line[0] in player_dict:  # Generates player_dict entries for new players
                pass
            else:
                player_entry_gen(line[0], line[1], line[5], '', '', line[2], '', line[3], line[4], '', '', '')

######################################## Left off here
def vital_grab(player):  # This function grabs player vital data from nba.com player profile pages.
    try:
        url = 'http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID='+player+'&SeasonType=Regular+Season'
        req = urlopen(url)
    except urllib.error.HTTPError as error_code:
        pass
    else:
        data = loads(req.read().decode())
        new_line = [item for item in data['resultSets'][0]['rowSet'][0]]
        height = new_line[10].split('-')  # Splits "height" string from feet-inches to [feet, inches]
        if len(height) > 1:  # Converts "height" string from feet and inches to meters
            player_dict[player]['height'] = (int(height[0])*12+int(height[1]))*.0254
        if new_line[11]:  # Converts weight from pounds to kilograms
            player_dict[player]['weight'] = int(new_line[11])*.453592
        player_dict[player]['approx_pos'] = new_line[14]
        # The following lines set individual DOB values to appropriate keys
        player_dict[player]['DOB']['year'] = new_line[6].split('-')[0]
        player_dict[player]['DOB']['month'] = new_line[6].split('-')[1]
        player_dict[player]['DOB']['day'] = new_line[6].split('-')[2][:2]


def vital_writer():  # Creating the vitals_csv from gathered information.
    header = ['PLAYER_ID', 'PLAYER_NAME', 'LISTED_POSITION', 'PLAYER_HEIGHT_M', 'PLAYER_WEIGHT_KG', 'ACTIVE_STATUS',
              'START_YEAR', 'END_YEAR', 'PLAYER_CODE', 'YEAR', 'MONTH', "DAY"]
    temp_cab = []
    for player in player_dict:
        if player_dict[player]['last_name'] == '':  # Nene check
            player_name = player_dict[player]['first_name']
        else:
            player_name = player_dict[player]['last_name']+', '+player_dict[player]['first_name']
        new_line = [player, player_name, player_dict[player]['approx_pos'], player_dict[player]['height'],
                    player_dict[player]['weight'], player_dict[player]['player_active'],
                    player_dict[player]['start_year'], player_dict[player]['end_year'],
                    player_dict[player]['player_code'], player_dict[player]['DOB']['year'],
                    player_dict[player]['DOB']['month'], player_dict[player]['DOB']['day']]
        temp_cab.append(new_line)
    temp_cab.sort(key=lambda x: x[1])  # Puts rows in alphabetical order by last name
    temp_cab.insert(0, header)
    with open('player_vitals.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(temp_cab)


if __name__ == '__main__':
    # This value sets directory destination for master id file
    player_id_movedir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\'
    # This value sets directory destination for player vital file
    player_vital_movedir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\physical data\\'
    player_dict = {}
    player_list_grabber()
    player_list_gen()
    for player_id in player_dict:
        print(player_id)
        if player_dict[player_id]['height']:  # Skips player_dict entries for existing players
            pass
        else:
            vital_grab(player_id)
            sleep(randint(1, 3))
    vital_writer()
    move('player_id_file.csv', player_id_movedir+'player_id_file.csv')
    move('player_vitals.csv', player_vital_movedir+'player_vitals.csv')
