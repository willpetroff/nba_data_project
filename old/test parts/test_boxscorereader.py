import csv
from statistics import pstdev
from statistics import pvariance
from statistics import mean

# Test program to return mean, stdev, and var for some shooting stats from a given team(s).
# Current settings are for the Houston Rockets and Los Angles Clippers-- see lines 23, 24, and references to 'hou_rost'
# and 'lac_rost'.


def games_pop(): #populates game id numbers for file names
    game_list = []
    for num in range(1, 1231):
        num_string = str(num)
        game_id = '00000'[len(num_string):]+num_string
        game_list.append(game_id)
    return game_list


def box_score_search(game): # Runs through box scores to find players on predefined teams and extract preselected data.
    file_dir = 'C:\\Users\\William\\Desktop\\Basketball Stats\\General Datasets\\basic nba.com data\\box score\\'
    file_name = '14_'+game+'_boxscore.csv'
    with open(file_dir+file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            if line[2] == 'HOU':
                two_fga = int(line[10])-int(line[13])
                two_fgm = int(line[9])-int(line[12])
                thr_fga = int(line[13])
                thr_fgm = int(line[12])
                fta = int(line[16])
                ftm = int(line[15])
                pts = int(line[26])
                if (two_fga+thr_fga) > 0:
                    efg = (two_fgm+(thr_fgm*1.5))/(two_fga+thr_fga)
                else:
                    efg = 0
                if line[5] not in hou_rost:
                    hou_rost[line[5]] = {game: {'2FGA': two_fga, '2FGM': two_fgm, '3FGA': thr_fga, '3FGM': thr_fgm,
                                                'FTA': fta, 'FTM': ftm, 'PTS': pts, 'eFG': efg}}
                else:
                    hou_rost[line[5]][game] = {'2FGA': two_fga, '2FGM': two_fgm, '3FGA': thr_fga, '3FGM': thr_fgm,
                                               'FTA': fta, 'FTM': ftm, 'PTS': pts, 'eFG': efg}
            if line[2] == 'LAC':
                two_fga = int(line[10])-int(line[13])
                two_fgm = int(line[9])-int(line[12])
                thr_fga = int(line[13])
                thr_fgm = int(line[12])
                fta = int(line[16])
                ftm = int(line[15])
                pts = int(line[26])
                if (two_fga+thr_fga) > 0:
                    efg = (two_fgm+(thr_fgm*1.5))/(two_fga+thr_fga)
                else:
                    efg = 0
                if line[5] not in lac_rost:
                    lac_rost[line[5]] = {game: {'2FGA': two_fga, '2FGM': two_fgm, '3FGA': thr_fga, '3FGM': thr_fgm,
                                                'FTA': fta, 'FTM': ftm, 'PTS': pts, 'eFG': efg}}
                else:
                    lac_rost[line[5]][game] = {'2FGA': two_fga, '2FGM': two_fgm, '3FGA': thr_fga, '3FGM': thr_fgm,
                                               'FTA': fta, 'FTM': ftm, 'PTS': pts, 'eFG': efg}


def consist_test(player): # Generates mean, stdev, and var data points for data pulled from box scores.
    two_fga = []
    two_fgm = []
    thr_fga = []
    thr_fgm = []
    fta = []
    ftm = []
    pts = []
    efg = []
    if player in hou_rost:
        for game in hou_rost[player]:
            two_fga.append(hou_rost[player][game]['2FGA'])
            two_fgm.append(hou_rost[player][game]['2FGM'])
            thr_fga.append(hou_rost[player][game]['3FGA'])
            thr_fgm.append(hou_rost[player][game]['3FGM'])
            fta.append(hou_rost[player][game]['FTA'])
            ftm.append(hou_rost[player][game]['FTM'])
            pts.append(hou_rost[player][game]['PTS'])
            efg.append(hou_rost[player][game]['eFG'])
    else:
        for game in lac_rost[player]:
            two_fga.append(lac_rost[player][game]['2FGA'])
            two_fgm.append(lac_rost[player][game]['2FGM'])
            thr_fga.append(lac_rost[player][game]['3FGA'])
            thr_fgm.append(lac_rost[player][game]['3FGM'])
            fta.append(lac_rost[player][game]['FTA'])
            ftm.append(lac_rost[player][game]['FTM'])
            pts.append(lac_rost[player][game]['PTS'])
            efg.append(lac_rost[player][game]['eFG'])
    con_two_fga = con_test(two_fga, player, '2fgm')
    con_two_fgm = con_test(two_fgm, player, '2fga')
    con_thr_fga = con_test(thr_fga, player, '3fga')
    con_thr_fgm = con_test(thr_fgm, player, '3fgm')
    con_fta = con_test(fta, player, 'fta')
    con_ftm = con_test(ftm, player, 'ftm')
    con_pts = con_test(pts, player, 'pts')
    con_efg = con_test(efg, player, 'efg')
    consist_score[player] = {'2FGA': con_two_fga, '2FGM': con_two_fgm, '3FGA': con_thr_fga, '3FGM': con_thr_fgm,
                           'FTA': con_fta, 'FTM': con_ftm, 'PTS': con_pts, 'eFG': con_efg}


def con_test(stat_list, player, stat_name): # Computes actual data points from data given via consist_test
    if stat_list:
        con_stat = (mean(stat_list), pvariance(stat_list), pstdev(stat_list))
        return con_stat
    else:
        print('NO DATA FOR: '+player+', '+stat_name)
        return 0


if __name__ == '__main__':
    game_list = games_pop()
    hou_rost = {}
    lac_rost = {}
    consist_score = {}
    for game in game_list:
        box_score_search(game)
    for player in hou_rost:
        consist_test(player)
    with open('con_scr_hou.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for player in consist_score:
            new_line = [player]
            for item in consist_score[player]:
                new_line.append(item)
                new_line.append(consist_score[player][item][0])
                new_line.append(consist_score[player][item][1])
                new_line.append(consist_score[player][item][2])
            writer.writerow(new_line)
    consist_score = {}
    for player in lac_rost:
        consist_test(player)
    with open('con_scr_lac.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for player in consist_score:
            new_line = [player]
            for item in consist_score[player]:
                new_line.append(item)
                new_line.append(consist_score[player][item][0])
                new_line.append(consist_score[player][item][1])
                new_line.append(consist_score[player][item][2])
            writer.writerow(new_line)
