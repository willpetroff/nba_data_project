import os
import csv


def top_words(event_list):
    for event in event_list:
        word_item = [item for item in event_list[event].items()]
        word_1 = (0, 0)
        word_2 = (0, 0)
        for item in word_item:
            if item[1] > word_1[1]:
                word_1 = item
            elif word_1[1] > item[1] > word_2[1]:
                word_2 = item
            else:
                pass
        print(str(event)+'\t'+str(word_1)+" and "+str(word_2))

top_lev_dir = "C:\\Python34\\projects\\nba scripts\\reading pbp\\pbp_total"
file_cab = os.listdir(top_lev_dir)
event_list = {num: {} for num in range(1, 20)}
for file in file_cab:
    with open(top_lev_dir+"\\"+file, 'r') as work_file:
        file_reader = csv.reader(work_file)
        next(file_reader)
        for line in file_reader:
            if line == []:
                pass
            else:
                line_1 = line[7].strip('():')
                line_2 = line[8].strip('():')
                line_3 = line[9].strip('():')
                word_list = line_1.split()+line_2.split()+line_3.split()
                for word in word_list:
                    if word in event_list[int(line[2])]:
                        event_list[int(line[2])][word] += 1
                    else:
                        event_list[int(line[2])][word] = 1

if __name__ == '__main__':
    top_words(event_list)
