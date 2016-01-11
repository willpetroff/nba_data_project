from urllib.request import urlopen
import csv
from json import loads
from shutil import move
                

def primary_grab(stat_type):
    url = 'http://stats.nba.com/js/data/sportvu/2014/'+stat_type+'Data.json'
    target_url = urlopen(url).read()
    data = loads(target_url.decode(encoding='UTF-8'))
    with open(stat_type+'.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header_cab = [data['resultSets'][0]['headers']]
        temp_cab = [item for item in data['resultSets'][0]['rowSet']]
        temp_cab.insert(0, header_cab[0])
        writer.writerows(temp_cab)


def main():
    stat_name = ['catchShoot', 'shooting', 'defense', 'rebounding', 'touches',
                 'passing', 'drives', 'pullUpShoot', 'speed']
    svu_data_movedir = 'C:\\Users\William\\Documents\\Python Projects\\nba\\data\\basic data\\svu data\\'
    for stat in stat_name:
        print(stat)
        primary_grab(stat)
        move(stat+'.csv', svu_data_movedir+stat+'.csv')


if __name__ == '__main__':
    main()
