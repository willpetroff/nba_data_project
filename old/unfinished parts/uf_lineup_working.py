import csv
from shutil import move
from time import localtime
import os


def player_mover(player_list, on_court_visitor, on_court_home):
    for player in player_list:
        if player not in home_roster:
            if player not in on_court_visitor:
                on_court_visitor.append(player)
        else:
            if player not in on_court_home:
                on_court_home.append(player)


def line_adder(num, line):
    line.append(pbp_dict[num]['game_id'])
    line.append(num)
    line.append(pbp_dict[num]['quarter'])
    line.append(pbp_dict[num]['time'])
    line.append(pbp_dict[num]['event_type'])
    line.append(pbp_dict[num]['event_action'])
    line.append(pbp_dict[num]['event'])
    line.append(pbp_dict[num]['home_score'])
    line.append(pbp_dict[num]['visitor_score'])
    line.append(pbp_dict[num]['home_net'])
    for player in pbp_dict[num]['on_court_h']:
        line.append(player)
    if len(pbp_dict[num]['on_court_h']) < 5:
        counter = len(pbp_dict[num]['on_court_h'])
        while counter < 5:
            line.append('')
            counter += 1
    for player in pbp_dict[num]['on_court_v']:
        line.append(player)
    if len(pbp_dict[num]['on_court_v']) < 5:
        counter = len(pbp_dict[num]['on_court_v'])
        while counter < 5:
            line.append('')
            counter += 1
    for player in pbp_dict[num]['players']:
        line.append(player)
    if len(pbp_dict[num]['players']) < 3:
        counter = len(pbp_dict[num]['players'])
        while counter < 3:
            line.append('')
            counter += 1
    line.append(pbp_dict[num]['dead_ball'])
    # line.append(pbp_dict[num]['line_error'])
    # line.append(pbp_dict[num]['home_players']+pbp_dict[num]['visitor_players'])


def time_eval(quarter, time_string):
    quarter_add = {'1': 2160, '2': 1440, '3': 720, '4': 0}
    time_parts = time_string.split(':')
    if int(quarter) > 4:
        quarter = '4'
    # print((int(time_parts[0])*60)+int(time_parts[1])+quarter_add[quarter])
    return (int(time_parts[0])*60)+int(time_parts[1])+quarter_add[quarter]


def id_generator(year):
    season_count = 1996
    for number in range(1, 1231):
        game_string = '00000'[:-len(str(number))]+str(number)
        games.append(game_string)
    while season_count < year:
        seasons.append(str(season_count)[2:4])
        season_count += 1


def size_check(season, game):
    file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\data\\basic data\\pbp\\'
    file_name = season+'_'+game+'_secondpass.csv'
    return os.path.getsize(file_dir+file_name)


def pbp_mem(season, game):
    file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\data\\basic data\\pbp\\'
    file_name = season+'_'+game+'_secondpass.csv'
    error_check = 0
    with open(file_dir+file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        count = 0
        for line in reader:
            pbp_dict[count] = {'time': line[6], 'quarter': line[4], 'event': '', 'on_court_h': [], 'on_court_v': [],
                               'players': [], 'dead_ball': 0, 'line_error': 0, 'home_players': 0, 'visitor_players': 0,
                               'event_type': line[2], 'event_action': line[3], 'home_score': line[10],
                               'visitor_score': line[11], 'home_net': line[12], 'game_id': line[0]}
            if line[7] and not line[9]:
                pbp_dict[count]['event'] = line[7]
            elif line[9] and not line[7]:
                pbp_dict[count]['event'] = line[9]
            elif line[7] and line[9]:
                pbp_dict[count]['event'] = line[7]+' AND '+line[9]
            elif line[2] == '13':
                pbp_dict[count]['event'] = 'END OF QUARTER '+line[4]
            else:
                pbp_dict[count]['event'] = 'NO EVENT'
            if line[15]:
                pbp_dict[count]['players'].append(line[15])
            if line[22]:
                pbp_dict[count]['players'].append(line[22])
            if line[29]:
                pbp_dict[count]['players'].append(line[29])
            count += 1
            if ('SUB:' in line[7] and not line[15]) or ('SUB:' in line[9] and not line[22]):
                error_check = 1
    for num in range(len(pbp_dict)):
        db_check = pbp_dict[num]['event'].upper().split()
        dead_ball_list = ['TIMEOUT:', 'TURNOVER', 'SUB:', 'OFF.FOUL', 'P.FOUL', 'FREE', 'B.FOUL', 'QUARTER']
        for word in dead_ball_list:
            if word == 'TURNOVER' and word in db_check and 'STEAL' not in db_check:
                pbp_dict[num]['dead_ball'] = 1
            elif word == 'FREE' and word in db_check and 'THROW' in db_check:
                if num+1 < len(pbp_dict) and 'REBOUND' not in pbp_dict[num+1]['event'].upper().split():
                    pbp_dict[num]['dead_ball'] = 1
            else:
                if word in db_check and word != 'TURNOVER' and word != 'FREE':
                    pbp_dict[num]['dead_ball'] = 1
    return error_check


def roster_builder(season, game):
    file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\box score\\'
    file_name = season+'_'+game+'_boxscore.csv'
    with open(file_dir+file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        vis_team = ''
        for line in reader:
            if not vis_team:
                vis_team = line[2]
            if line[2] == vis_team:
                if line[6]:
                    visitor_starters.append(line[5])
                visitor_roster.append(line[5])
            else:
                if line[6]:
                    home_starters.append(line[5])
                home_roster.append(line[5])


def lineup_test(season, game):
    roster_builder(season, game)
    on_court_home = []
    on_court_visitor = []
    for num in range(len(pbp_dict)):
        if num == 0:
            pbp_dict[num]['on_court_h'] = home_starters
            pbp_dict[num]['on_court_v'] = visitor_starters
        else:
            if pbp_dict[num-1]['event'] == 'END OF QUARTER 2':
                pbp_dict[num]['on_court_h'] = home_starters
                pbp_dict[num]['on_court_v'] = visitor_starters
            elif pbp_dict[num]['dead_ball'] == 1 and 'SUB:' in pbp_dict[num]['event'].split():
                on_court_home = []
                on_court_visitor = []
                if pbp_dict[num]['players'][1] not in home_roster:
                    on_court_visitor.append(pbp_dict[num]['players'][1])
                else:
                    on_court_home.append(pbp_dict[num]['players'][1])
                pbp_dict[num]['on_court_v'] = on_court_visitor
                pbp_dict[num]['on_court_h'] = on_court_home
            elif pbp_dict[num]['dead_ball'] == 1 and 'SUB:' not in pbp_dict[num]['event'].split():
                player_mover(pbp_dict[num]['players'], on_court_visitor, on_court_home)
                pbp_dict[num]['on_court_v'] = on_court_visitor
                pbp_dict[num]['on_court_h'] = on_court_home
                on_court_home = []
                on_court_visitor = []
            else:
                if pbp_dict[num-1]['dead_ball'] == 1 and 'SUB:' not in pbp_dict[num-1]['event'].split():
                    on_court_home = []
                    on_court_visitor = []
                else:
                    on_court_home = pbp_dict[num-1]['on_court_h']
                    on_court_visitor = pbp_dict[num-1]['on_court_v']
                player_mover(pbp_dict[num]['players'], on_court_visitor, on_court_home)
                pbp_dict[num]['on_court_h'] = on_court_home
                pbp_dict[num]['on_court_v'] = on_court_visitor
        if len(pbp_dict[num]['on_court_h']) > 5 or len(pbp_dict[num]['on_court_v']) > 5:
            pbp_dict[num]['line_error'] = 1
        pbp_dict[num]['home_players'] = len(pbp_dict[num]['on_court_h'])
        pbp_dict[num]['visitor_players'] = len(pbp_dict[num]['on_court_v'])


def back_track(season, game):
    pbp_list = [num for num in range(len(pbp_dict))]
    pbp_list.reverse()
    for num in pbp_list:
        if (num+1) in pbp_dict:
            if pbp_dict[num]['dead_ball'] == 0:
                for player in pbp_dict[num+1]['on_court_h']:
                    if player not in pbp_dict[num]['on_court_h']:
                        pbp_dict[num]['on_court_h'].append(player)
                for player in pbp_dict[num+1]['on_court_v']:
                    if player not in pbp_dict[num]['on_court_v']:
                        pbp_dict[num]['on_court_v'].append(player)
    with open(season+'_'+game+'_thirdpass.csv', 'w', newline='') as new_csv:
        writer = csv.writer(new_csv)
        header_cab = ['GAME_ID', 'PLAY_NUM', 'QUARTER', 'TIME', 'EVENT_TYPE', 'ACTION_TYPE', 'EVENT', 'HOME_SCORE',
                      'VISITOR_SCORE', 'NET_SCORE_H', 'HOME_P1', 'HOME_P2', 'HOME_P3', 'HOME_P4', 'HOME_P5',
                      'VISITOR_P1', 'VISITOR_P2', 'VISITOR_P3', 'VISITOR_P4', 'VISITOR_P5', 'ACTION_P1', 'ACTION_P2',
                      'ACTION_P3', 'DEAD_BALL']
        writer.writerow(header_cab)
        pbp_list.reverse()
        for num in pbp_list:
            new_line = []
            line_adder(num, new_line)
            writer.writerow(new_line)


def time_collector(season, game):
    with open(season+'_'+game+'_test.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        pbp_cab = []
        for line in reader:
            pbp_cab.append(line)
        for index in range(1, len(pbp_cab)):
            previous_home = [pbp_cab[index-1][10], pbp_cab[index-1][11], pbp_cab[index-1][12], pbp_cab[index-1][13],
                             pbp_cab[index-1][14]]
            previous_vis = [pbp_cab[index-1][15], pbp_cab[index-1][16], pbp_cab[index-1][17], pbp_cab[index-1][18],
                            pbp_cab[index-1][19]]
            oc_home = [pbp_cab[index][10], pbp_cab[index][11], pbp_cab[index][12], pbp_cab[index][13],
                       pbp_cab[index][14]]
            oc_vis = [pbp_cab[index][15], pbp_cab[index][16], pbp_cab[index][17], pbp_cab[index][18],
                      pbp_cab[index][19]]
            for player in oc_home:
                if player:
                    if player in previous_home:
                        if player not in home_time:
                            home_time[player] = (time_eval(pbp_cab[index-1][2], pbp_cab[index-1][3]) -
                                                 time_eval(pbp_cab[index][2], pbp_cab[index][3]))
                        else:
                            home_time[player] = (time_eval(pbp_cab[index-1][2], pbp_cab[index-1][3]) -
                                                 time_eval(pbp_cab[index][2], pbp_cab[index][3]))
            for player in oc_vis:
                if player:
                    if player in previous_vis:
                        if player not in visitor_time:
                            visitor_time[player] = (time_eval(pbp_cab[index-1][2], pbp_cab[index-1][3]) -
                                                    time_eval(pbp_cab[index][2], pbp_cab[index][3]))
                        else:
                            visitor_time[player] += (time_eval(pbp_cab[index-1][2], pbp_cab[index-1][3]) -
                                                     time_eval(pbp_cab[index][2], pbp_cab[index][3]))


def file_mover(season, game):
    file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\data\\basic data\\pbp\\third pass\\'
    old_file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\data\\basic data\\pbp\\'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    file_name = season+'_'+game+'_thirdpass.csv'
    move(file_name, file_dir+file_name)
    if os.path.exists(file_dir+file_name):
        os.remove(old_file_dir+file_name)


if __name__ == '__main__':
    seasons = []
    games = []
    error_files = []
    empty_files = []
    id_generator(localtime()[0])
    for season_id in seasons:
        for game_id in games:
            size_flag = size_check(season_id, game_id)
            if size_flag > 100:
                print(season_id, game_id)
                pbp_dict = {}
                home_starters = []
                visitor_starters = []
                home_roster = []
                visitor_roster = []
                temp_cab = []
                home_time = {}
                visitor_time = {}
                error_flag = pbp_mem(season_id, game_id)
                if error_flag != 1:
                    lineup_test(season_id, game_id)
                    back_track(season_id, game_id)
                    # time_collector(season_id, game_id)
                    file_mover(season_id, game_id)
                else:
                    error_files.append([season_id, game_id])
            else:
                empty_files.append([season_id, game_id])
    with open('error_files.csv', 'w', newline='') as new_file:
        error_writer = csv.writer(new_file)
        for file in error_files:
            file.append('ERROR IN FILE')
            error_writer.writerow(file)
        for file in empty_files:
            file.append('EMPTY FILE')
            error_writer.writerow(file)
