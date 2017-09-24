import csv
import os
from time import time


def time_conversion(time_parts):
    temp_list = time_parts[0].split(':')
    quarter_count = time_parts[1]
    if quarter_count == 1:
        time_add = 36*60
    elif quarter_count == 2:
        time_add = 24*60
    elif quarter_count == 3:
        time_add = 12*60
    else:
        time_add = 0
    seconds = int(temp_list[0])*60+int(temp_list[1])+time_add
    return seconds


def pbp_test(test_index):
    for item in test_index:
        if item[-1][2] == '2':
            print("The last play is a miss")
        else:
            print("ERROR!")
            print(item)
    

top_lev_dir = 'C:\\Python34\\projects\\nba scripts\\reading pbp\\pbp_total'
file_cab = os.listdir(top_lev_dir)
large_time = 0
for file in file_cab:
    with open(top_lev_dir+"\\"+file, 'r') as work_file:
        file_reader = csv.reader(work_file)
        next(file_reader)
        play_by_play = []
        start_time = [0, 0]
        end_time = [0, 0]
        cut_counter = 0
        index_counter = 1
        for line in file_reader:
            if len(line) > 0:
                play_by_play.append(line)
            else:
                pass
        start_time = [play_by_play[0][6], play_by_play[0][4]]
        for play in play_by_play:
            if play[2] == '2':
                end_time = [play[6], play[4]]
                elapsed_time = time_conversion(start_time)-time_conversion(end_time)
                if elapsed_time > large_time:
                    large_time_pbp = [play_by_play[0:index_counter], file]
                    time_list = [start_time, end_time]
                    large_time = elapsed_time
                    print("The new large_time is: "+str(large_time))
                play_by_play = play_by_play[cut_counter+1:]
                cut_counter = 0
                index_counter = 1
                if play[4] == '4' and play[6] == '0:00':
                    pass
                else:
                    start_time = [play_by_play[0][6], play_by_play[0][4]]
            else:
                index_counter += 1
                cut_counter += 1


print(large_time_pbp[1])
print(large_time/60)
print(time_list)
