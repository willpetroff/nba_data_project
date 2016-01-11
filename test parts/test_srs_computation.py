import csv
# import urllib.request
import numpy as np
import os


def path_check(path):
    if 'srs_data' not in os.listdir(path):
        print('make srs path')
        os.makedirs(path+'\\srs_data')
    if 'game_data' not in os.listdir(path+'\\srs_data\\'):
        os.makedirs(path+'\\srs_data\\game_data')
    if 'srs_final' not in os.listdir(path+'\\srs_data\\'):
        os.makedirs(path+'\\srs_data\\srs_final')


def srs_data_fetch(year, path):
    box_score_path = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\box score'
    games = []
    for item in os.listdir(box_score_path):
        if year == item[:2]:
            with open(box_score_path+'\\'+item, 'r') as box_score_csv:
                reader = csv.reader(box_score_csv)
                team_away = ''
                team_home = ''
                away_score = 0
                home_score = 0
                for line in reader:
                    if not team_away:
                        team_away = line[2]
                    if line[2] == team_away:
                        away_score += int(line[26])
                    else:
                        team_home = line[2]
                        home_score += int(line[26])
                games.append([team_home, team_away, home_score, away_score])
    with open(path+'\\srs_data\\game_data\\'+year+'_srs_data.csv', 'w', newline='') as games_csv:
        writer = csv.writer(games_csv)
        writer.writerows(games)


def home_court_adv(year, path):
    home_score = []
    away_score = []
    reverse_list = ['76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91',
                    '92', '93', '94', '95']
    with open(path+'\\srs_data\\game_data\\'+year+'_srs_data.csv', 'r',) as srs_csv:
        reader = csv.reader(srs_csv)
        for line in reader:
            if year not in reverse_list:
                home_score.append(int(line[2]))
                away_score.append(int(line[3]))
            else:
                home_score.append(int(line[3]))
                away_score.append(int(line[2]))
    home_court_avg_mov = (sum(home_score)/len(home_score))-(sum(away_score)/len(away_score))
    return home_court_avg_mov


def srs_formatting(year, path, home_court=3.2167):
    reverse_list = ['76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91',
                    '92', '93', '94', '95']
    teams = {}
    home_court_advantage = home_court
    with open(path+'\\srs_data\\game_data\\'+year+'_srs_data.csv', 'r',) as srs_csv:
        reader = csv.reader(srs_csv)
        for line in reader:
            if year not in reverse_list:
                team_home = line[0]
                team_away = line[1]
                home_mov = (int(line[2])-home_court_advantage) - int(line[3])
                away_mov = - home_mov
                if int(line[2])-int(line[3]) > 0:
                    home_win = 1
                    away_win = 0
                else:
                    away_win = 1
                    home_win = 0
            else:
                team_home = line[1]
                team_away = line[0]
                home_mov = (int(line[3])-home_court_advantage)-int(line[2])
                away_mov = -home_mov
                if int(line[3])-int(line[2]) > 0:
                    home_win = 1
                    away_win = 0
                else:
                    home_win = 0
                    away_win = 1
            if team_home in teams:
                teams[team_home]['mov'].append(home_mov)
                teams[team_home]['opp'].append(team_away)
                teams[team_home]['wins'] += home_win
            else:
                teams[team_home] = {'average_mov': 0, 'mov': [home_mov], 'opp': [team_away], 'wins': home_win}
            if team_away in teams:
                teams[team_away]['mov'].append(away_mov)
                teams[team_away]['opp'].append(team_home)
                teams[team_away]['wins'] += away_win
            else:
                teams[team_away] = {'average_mov': 0, 'mov': [away_mov], 'opp': [team_away], 'wins': away_win}
    for team in teams:
        teams[team]['average_mov'] = sum(item for item in teams[team]['mov'])/len(teams[team]['mov'])
    return teams


def srs_calculation(team_dict):
    terms = []
    solutions = []
    team_order = []
    for team in team_dict:
        row = []
        for opp_team in team_dict:
            if opp_team == team:
                row.append(-1)
            elif opp_team in team_dict[team]['opp']:
                count = 0
                for item in team_dict[team]['opp']:
                    if opp_team == item:
                        count += 1
                row.append(count/len(team_dict[team]['opp']))
            else:
                row.append(0)
        terms.append(row)
        solutions.append(-team_dict[team]['average_mov'])
        team_order.append(team)
    array_terms = np.array(terms)
    array_solutions = np.array(solutions)
    srs = np.linalg.solve(array_terms, array_solutions)
    srs_cab = [item for item in srs]
    for index in range(len(team_order)):
        team_dict[team_order[index]]['srs'] = srs_cab[index]
    return team_dict


def main():
    year_dict = {item[:2]: item[:2] for item in os.listdir('C:\\Users\\William\\Documents\\Python Projects\\nba\\'
                                                           'data\\basic data\\box score')}
    srs_path = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data'
    hca = []
    path_check(srs_path)
    for srs_year in year_dict:
        srs_data_fetch(srs_year, srs_path)
        home_mov = home_court_adv(srs_year, srs_path)
        hca.append([srs_year, home_mov])
        temp_dict = srs_formatting(srs_year, srs_path, home_mov)
        final_dict = srs_calculation(temp_dict)
        csv_cab = []
        net_point_val = .000400683977747551
        for team in final_dict:
            estimated_wins = (((final_dict[team]['srs']*82)*net_point_val)*82)+41
            csv_cab.append([team, final_dict[team]['srs'], estimated_wins, final_dict[team]['wins'],
                            final_dict[team]['average_mov']])
        with open(srs_path+'\\srs_data\\srs_final\\'+srs_year+'_srs_final.csv', 'w', newline='') as srs_csv:
            writer = csv.writer(srs_csv)
            writer.writerows(csv_cab)
    with open(srs_path+'\\srs_data\\hca_year.csv', 'w', newline='') as hca_csv:
        writer = csv.writer(hca_csv)
        writer.writerows(hca)


if __name__ == '__main__':
    main()
