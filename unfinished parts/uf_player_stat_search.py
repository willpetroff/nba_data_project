import csv


def stat_index(stat_string): #returns index value for a given statistic from
    stat_index_value = {'assist': 21, 'points': 26, 'steals': 22, 'blocks': 23, "turnovers": 24, "fouls": 25,
                        'orebounds': 18, 'drebounds': 19, 'fga': 10, 'fgm': 9, '3fga': 13, '3fgm': 12, 'fta': 16,
                        'ftm': 15}
    if stat_string in stat_index_value:
        return stat_index_value[stat_string]


def stat_compiler(stat, player):
    index_value = stat_index(stat)
