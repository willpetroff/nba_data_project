'''
still needs to fix overtime problems
'''

import csv
import os


def time_conversion(time_parts):
    temp_list = time_parts[0].split(':')
    quarter_count = int(time_parts[1])
    if quarter_count <= 4:
        if quarter_count == 1:
            time_add = 36*60
        elif quarter_count == 2:
            time_add = 24*60
        elif quarter_count == 3:
            time_add = 12*60
        else:
            time_add = 0
        seconds = int(temp_list[0])*60+int(temp_list[1])+time_add
    else:
        seconds = -((5*60)-(int(temp_list[0])*60+int(temp_list[1])))
    return seconds


def time_til_20(play_string, score_list):
    start_time = time_conversion([play_string[1], play_string[0]])
    elapsed_time = 999999999999
    if len(score_list) < 2:
        return elapsed_time
    if score_list[1][2] == play_string[2]:
        return elapsed_time
    else:
        for play in score_list:
            if int(play[2])-int(play_string[2]) < 20:
                pass
            else:
                elapsed_time = start_time - time_conversion([play[1], play[0]])
                return elapsed_time
    return elapsed_time


file_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\pbp'
file_cab = os.listdir(file_dir)
elapsed_time_20 = [['', 9999999, ['', '']]]
for file in file_cab:
    print(file)
    if file == 'third pass':
        pass
    else:
        with open(file_dir + '\\' + file, 'r') as pbp_file:
            home_score = []
            vis_score = []
            reader = csv.reader(pbp_file)
            next(reader)
            for line in reader:
                home_score.append([line[4], line[6], line[10]])
                vis_score.append([line[4], line[6], line[11]])
        home_score_master = home_score[:]
        vis_score_master = vis_score[:]
        for item in home_score_master:
            temp_time_h = time_til_20(item, home_score)
            if temp_time_h == elapsed_time_20[0][1]:
                elapsed_time_20.append([file, temp_time_h, [item[0], item[1]]])
            elif temp_time_h < elapsed_time_20[0][1]:
                elapsed_time_20 = [[file, temp_time_h, [item[0], item[1]]]]
            home_score.pop(0)
        for item in vis_score_master:
            temp_time_v = time_til_20(item, vis_score)
            if temp_time_v == elapsed_time_20[0][1]:
                elapsed_time_20.append([[file, temp_time_v, [item[0], item[1]]]])
            elif temp_time_v < elapsed_time_20[0][1]:
                elapsed_time_20 = [[file, temp_time_v, [item[0], item[1]]]]
            vis_score.pop(0)
print(elapsed_time_20)
