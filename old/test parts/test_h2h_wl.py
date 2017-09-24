import csv
from os import listdir
import urllib.request
from json import loads
import time
from random import randint


def jordan_check(file, top_level_dir):
    print(file)
    jordan_in = 0
    with open(top_level_dir+'\\'+file, 'r') as box_score:
        reader = csv.reader(box_score)
        player_list = [line[5] for line in reader]
        if 'Michael Jordan' in player_list:
            jordan_in = 1
    if jordan_in == 1:
        with open(top_level_dir+'\\'+file, 'r') as box_score:
            reader = csv.reader(box_score)
            file_cab = [line for line in reader]
            record_test(file_cab)


def record_test(box_score_line):
    team_a = 0
    team_b = 0
    team_a_name = box_score_line[0][2]
    print(team_a_name)
    team_a_win = 0
    for line in box_score_line:
        if line[2] == team_a_name:
            team_a += int(line[26])
        else:
            team_b += int(line[26])
    if team_a > team_b:
        team_a_win = 1
        print(team_a, team_b, team_a_win)
    record_counter(team_a_name, team_a_win, box_score_line)


def record_counter(first_team_name, first_team_win, box_score_info):
    box_score_dict = {line[5]: line[2] for line in box_score_info}
    if box_score_dict['Michael Jordan'] == first_team_name:
        win_value = first_team_win
    else:
        if first_team_win == 1:
            win_value = 0
        else:
            win_value = 1
    for player in box_score_dict:
        if box_score_dict[player] != box_score_dict['Michael Jordan']:
            if player in master_player_record:
                if win_value == 1 and box_score_dict['Michael Jordan'] == 'CHI':
                    master_player_record[player]['lossChi'] += 1
                elif win_value == 0 and box_score_dict['Michael Jordan'] == 'CHI':
                    master_player_record[player]['winChi'] += 1
                elif win_value == 1 and box_score_dict['Michael Jordan'] != 'CHI':
                    master_player_record[player]['lossWiz'] += 1
                elif win_value == 0 and box_score_dict['Michael Jordan'] != 'CHI':
                    master_player_record[player]['winWiz'] += 1
            else:
                if win_value == 1 and box_score_dict['Michael Jordan'] == 'CHI':
                    master_player_record[player] = {'winWiz': 0, 'lossWiz': 0, 'winChi': 0, 'lossChi': 1}
                elif win_value == 0 and box_score_dict['Michael Jordan'] == 'CHI':
                    master_player_record[player] = {'winWiz': 0, 'lossWiz': 0, 'winChi': 1, 'lossChi': 0}
                elif win_value == 1 and box_score_dict['Michael Jordan'] != 'CHI':
                    master_player_record[player] = {'winWiz': 0, 'lossWiz': 1, 'winChi': 0, 'lossChi': 0}
                elif win_value == 0 and box_score_dict['Michael Jordan'] != 'CHI':
                    master_player_record[player] = {'winWiz': 1, 'lossWiz': 0, 'winChi': 0, 'lossChi': 0}


def win_loss_check(player_record):
    line_cab = []
    for player in player_record:
        player_per_tot = (player_record[player]['winWiz'] + player_record[player]['winChi']) /\
                         (player_record[player]['winWiz'] + player_record[player]['lossWiz'] +
                          player_record[player]['winChi'] + player_record[player]['lossChi'])
        player_per_chi = 0
        player_per_wiz = 0
        if (player_record[player]['winWiz'] + player_record[player]['lossWiz']) > 0:
            player_per_wiz = player_record[player]['winWiz'] /\
                             (player_record[player]['winWiz'] + player_record[player]['lossWiz'])
        if (player_record[player]['winChi'] + player_record[player]['lossChi']) > 0:
            player_per_chi = player_record[player]['winChi'] /\
                             (player_record[player]['winChi'] + player_record[player]['lossChi'])
        player_win_tot = player_record[player]['winWiz'] + player_record[player]['winChi']
        line_cab.append([player, player_win_tot, player_per_tot, player_record[player]['winChi'],
                         player_record[player]['lossChi'], player_per_chi, player_record[player]['winWiz'],
                         player_record[player]['lossWiz'], player_per_wiz])
    with open('best_wins.csv', 'w', newline='') as result_file:
        writer = csv.writer(result_file)
        writer.writerows(line_cab)


def name_pop(year):
    season_count = 1976
    for number in range(1, 1231):
        game_string = '00000'[:-len(str(number))]+str(number)
        games.append(game_string)
    while season_count < year:
        seasons.append(str(season_count)[2:4])
        season_count += 1


def box_score_scraper(season, game):
    # print ('in box scraper module')
    file_header = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\box score'
    url = 'http://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange=288000&GameID=002' + season + game +\
        '&RangeType=2&Season=2011-12&SeasonType=Regular+Season&StartPeriod=1&StartRange=0'
    with open(file_header + '\\' + season + '_' + game + '_boxscore.csv', 'w', newline='')as csv_file:
        try:
            req = urllib.request.urlopen(url)
        except urllib.request.HTTPError:
            pass
        else:
            data = loads(req.read().decode())
            temp_cab = [item for item in data['resultSets'][0]['rowSet']]
            # header_cab = [item for item in data['resultSets'][0]['headers']]
            # temp_cab.insert(0, header_cab)
            writer = csv.writer(csv_file)
            writer.writerows(temp_cab)
    time.sleep(randint(1, 2))

if __name__ == '__main__':
    seasons = []
    games = []
    name_pop(time.localtime()[0])
    for season_id in seasons:
        for game_id in games:
            print(season_id, game_id)
            box_score_scraper(season_id, game_id)
        time.sleep(randint(10, 20))
    master_player_record = {}
    file_folder = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\box score'
    for file_name in listdir(file_folder):
        jordan_check(file_name, file_folder)
    win_loss_check(master_player_record)
