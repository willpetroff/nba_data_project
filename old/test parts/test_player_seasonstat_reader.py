import csv


def player_check(player_id):
    file_path = 'C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\basic data\\player regular season\\'
    file_name = player_id+'_regular_season_totals.csv'
    player_stats = {}
    season_counter = 1
    with open(file_path + file_name, 'r') as player_csv_file:
        player_reader = csv.reader(player_csv_file)
        next(player_reader)
        for season in player_reader:
            try:
                player_stats[season_counter] = {'games': int(season[6]), 'pts': float(season[26]),
                                                'ast': float(season[21]), 'reb': float(season[20])}
            except ValueError:
                pass
            season_counter += 1
    return player_stat_adder(player_stats)


def player_stat_adder(stat_dict):
    total_games = sum(stat_dict[stat]['games'] for stat in stat_dict)
    avg_pts = sum(stat_dict[stat]['pts']*(stat_dict[stat]['games']/total_games) for stat in stat_dict)
    avg_ast = sum(stat_dict[stat]['ast']*(stat_dict[stat]['games']/total_games) for stat in stat_dict)
    avg_reb = sum(stat_dict[stat]['reb']*(stat_dict[stat]['games']/total_games) for stat in stat_dict)
    print(avg_pts, avg_reb, avg_ast)
    if avg_pts >= 24:
        if avg_ast >= 4:
            if avg_reb >= 4:
                print('Yes')
                return True


if __name__ == '__main__':
    player_ids = {}
    counter = 0
    with open('C:\\Users\\William\\Documents\\Python Projects\\nba\\data\\player_id_file.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for item in reader:
            player_ids[item[0]] = item[1]
    for item in player_ids:
        print(item)
        if player_check(item):
            counter += 1
            print(player_ids[item])
    print(counter)
