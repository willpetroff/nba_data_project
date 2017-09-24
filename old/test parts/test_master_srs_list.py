"""
Python 3.4.3

Creates master list for SRS ratings.

Created 12/22/15
"""
import csv
import os

srs_dir = 'C:\\Users\\William\\Documents\\Python Projects\\nba\data\\basic data\\srs_data\\srs_final\\'
master_file = []
season_list = [item for item in os.listdir(srs_dir)]
for item in season_list:
    with open(srs_dir+item, 'r') as srs_csv:
        reader = csv.reader(srs_csv)
        for line in reader:
            master_file.append([item[:2]+line[0], line[1]])
with open('srs_master_file.csv', 'w', newline='') as master_csv:
    writer = csv.writer(master_csv)
    writer.writerows(master_file)