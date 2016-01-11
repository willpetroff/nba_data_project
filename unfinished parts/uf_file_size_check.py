import os
import csv


def file_list(dir_path):
    file_list = []
    for file in os.listdir(dir_path):
        file_list.append(file)
    return file_list


def main():
    file_path = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\box score'
    empty_bs_list = []
    box_score_list = file_list(file_path)
    for file in box_score_list:
        if os.path.getsize(file_path+'\\'+file) == 0:
            empty_bs_list.append([file])
    with open('empty_box_score.csv', 'w', newline='') as error_csv:
        writer = csv.writer(error_csv)
        writer.writerows(empty_bs_list)
    return empty_bs_list


if __name__ == '__main__':
    team_list = {'Atlanta': 1976, 'Boston': 1976, 'Charlotte': 2004, 'Chicago': 1976, 'Cleveland': 1976, 'Dallas': 1980,
                 'Denver': 1976, 'Detroit': 1976, 'Golden State': 1976, 'Houston': 1976, 'Indiana': 1976, 'LAC': 1976,
                 'LAL': 1976, 'Milwaukee': 1976, 'Memphis': 1995, 'Miami': 1988, 'Minnesota': 1989, 'Brooklyn': 1976,
                 'NOP': 1988, 'NYK': 1976, 'Orlando': 1989, 'Philadelphia': 1976, 'Phoenix': 1976, 'Portland': 1976,
                 'Sacramento': 1976, 'San Antonio': 1976, 'Oklahoma City': 1976, 'Toronto': 1995, 'Utah': 1976,
                 'Washington': 1976}
    seasons_game = {}
    seasons = [year for year in range(1976, 2015)]
    for season in seasons:
        team_count = len([team for team in team_list if team_list[team] <= season])
        if season == 1998:
            game_num = 50
        elif season == 2011:
            game_num = 66
        else:
            game_num = 82
        game_count = (team_count/2)*game_num
        seasons_game[str(season)[2:]] = int(game_count)
    empty = main()
    for item in empty:
        item_path = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\box score\\'+item[0]
        season = item[0][:2]
        game = item[0][3:8]
        if int(game) > seasons_game[season] and os.path.getsize(item_path) == 0:
            os.remove(item_path)