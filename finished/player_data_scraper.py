"""
Python 3.4.3

This is a script that gets the json file that contains all NBA players and their ID numbers from nba.com and edits it
into a manageable format.

Created: 5/20/14
Edited: 10/19/15
*Moved file creation from beginning to end
*Created player_entry_gen
*Made script updating rather than refreshing
Edited: 11/10/15
*Set default values on player_list_grabber function
"""
from urllib.request import urlopen
from json import loads
import csv
from shutil import move
from time import sleep
from random import randint
from os import listdir
from time import localtime


def player_list_grabber(year1=localtime()[0], year2=localtime()[0]+1):  # Year1, Year2 default to present year and +1
    season_id = str(year1)+'-'+str(year2)[2:]
    url = 'http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=0&LeagueID=00&Season='+season_id
    req = urlopen(url)
    data = loads(req.read().decode())
    header_cab = [data['resultSets'][0]['headers']]  # Sets aside header values from nba json file
    temp_cab = [item for item in data['resultSets'][0]['rowSet']]  # Builds player list
    temp_cab.insert(0, header_cab[0])
    with open('player_id_file.csv', 'w', newline='') as id_file:
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
    if 'player_vitals.csv' in listdir('C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\physical data'):
        with open('C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\physical data\\player_vitals.csv', 'r')\
                as player_vital_file:
            reader = csv.reader(player_vital_file)
            next(reader)
            for line in reader:  # Generates player_dict entries for existing players
                player_entry_gen(line[0], line[1], line[8], line[3], line[4], line[5], line[2], line[6], line[7],
                                  line[9], line[10], line[11])
    with open('player_id_file.csv', 'r') as id_file:
        reader = csv.reader(id_file)
        next(reader)
        for line in reader:
            if line[0] in player_dict:  # Generates player_dict entries for new players
                pass
            else:
                player_entry_gen(line[0], line[1], line[5], '', '', line[2], '', line[3], line[4], '', '', '')


def vital_grab(player):  # This function grabs player vital data from nba.com player profile pages.
    url = 'http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID='+player+'&SeasonType=Regular+Season'
    req = urlopen(url)
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
