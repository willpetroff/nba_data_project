import requests

from datetime import date


class NBADataScraper(object):

    def __init__(self):
        self.CURRENT_SEASON = self._get_current_season()
        self.header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0",
                       'Accept-Encoding': "gzip, deflate",
                       'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       'Host': "stats.nba.com",
                       'Connection': "keep-alive",
                       'origin': ('http://stats.nba.com')}

    # No Error Check
    # split ?
    # shot_clock_range
    # playoff_round ?
    # opponent_team_id
    # location
    # def get_individual_player_stats(self, player_id, date_from="", date_to="", game_segment="", last_n_games=0,
    #                                 league_id="00", location="", measure_type="Base", month=0, opponent_team_id=0,
    #                                 outcome="", playoff_round=0, pace_adjusted="N", per_type="PerGame", period=0,
    #                                 plus_minus="N", rank="N", season="", season_segment="",
    #                                 season_type="Regular+Season", shot_clock_range="", split="yoy", vs_conference="",
    #                                 vs_division=""):
    #     print("In get_individual_player_stats")
    #     season = season if season else self.CURRENT_SEASON
    #     game_segment = self._capitalize_word(game_segment, split_on="+")
    #     measure_type = self._capitalize_word(measure_type, split_on="+")
    #     outcome = outcome.upper()
    #     pace_adjusted = pace_adjusted.upper()
    #     season_segment = self._capitalize_word(season_segment, split_on="+")
    #     season_type = self._capitalize_word(season_type, split_on="+")
    #     vs_conference = self._capitalize_word(vs_conference)
    #     vs_division = self._capitalize_word(vs_division)
    #     # GAME_SEGMENT
    #     if game_segment and game_segment not in ["First+Half", "Second+Half", "Overtime"]:
    #         raise ValueError('GAME_SEGMENT must be either "First+Half", "Second+Half", or "Overtime"')
    #     # LAST_N_GAMES
    #     if type(last_n_games) != int:
    #         raise ValueError('LAST_N_GAMES must be an integer')
    #     # LEAGUE_ID
    #     if league_id not in ["00", "20"]:
    #         raise ValueError('LEAGUE_ID must be "00" or "20"')
    #     # MEASURE_TYPE
    #     if measure_type and measure_type not in ["Base", "Advanced", "Misc", "Four+Factors", "Scoring", "Opponent",
    #                                              "Usage"]:
    #         raise ValueError('MEASURE_TYPE must be "Base", "Advanced", "Misc", "Four+Factors", "Scoring", "Opponent",'
    #                          ' "Usage"')
    #     # MONTH
    #     if type(month) != int:
    #         raise ValueError('MONTH must be an integer')
    #     if 0 > month > 12:
    #         raise ValueError('MONTH must be a value between 0 and 12')
    #     # OUTCOME
    #     if outcome and outcome not in ["W", "L"]:
    #         raise ValueError('OUTCOME must be either "W" or "L"')
    #     # PACE_ADJUSTED
    #     if pace_adjusted and pace_adjusted not in ["Y", "N"]:
    #         raise ValueError('PACE_ADJUSTED must be either "Y" or "N"')
    #     # PER_TYPE
    #     if per_type and per_type.lower() not in ["totals", "pergame", "minutesper", "per48", "per40", "per36",
    #                                              "perminute", "perpossession", "perplay", "per100posessions",
    #                                              "per100plays"]:
    #         raise ValueError('PER_TYPE must be either "totals", "pergame", "minutesper", "per48", "per40", "per36",'
    #                          ' "perminute", "perpossession", "perplay", "per100posessions", "per100plays"')
    #     # PERIOD
    #     if type(period) != int:
    #         raise ValueError('PERIOD must be an integer')
    #     # PLUS_MINUS
    #     if plus_minus and plus_minus not in ["Y", "N"]:
    #         raise ValueError('PLUS_MINUS must be either "Y" or "N"')
    #     # RANK
    #     if rank and rank not in ["Y", "N"]:
    #         raise ValueError('RANK must be either "Y" or "N"')
    #     # SEASON_SEGMENT
    #     if season_segment and season_segment.lower() not in ["pre+all-star", "post+all-star"]:
    #         raise ValueError('SEASON_SEGMENT must be either "Regular+Season", "Pre+Season", or "Playoffs"')
    #     # SEASON_TYPE
    #     if season_type and season_type not in ["Regular+Season", "Pre+Season", "Playoffs"]:
    #         raise ValueError('SEASON_TYPE must be either "Regular+Season", "Pre+Season", or "Playoffs"')
    #     # SHOT_CLOCK_RANGE
    #     # ((24-22)|(22-18 Very Early)|(18-15 Early)|(15-7 Average)|(7-4 Late)|(4-0 Very Late)|(ShotClock Off))
    #     # VS_CONFERENCE
    #     if vs_conference and vs_conference not in ['East', 'West']:
    #         raise ValueError('VS_CONFERENCE must be either "East" or "West"')
    #     # VS_DIVISION
    #     if vs_division and vs_division not in ['Atlantic', 'Central', 'Northwest', 'Pacific', 'Southeast', 'East',
    #                                            'West']:
    #         raise ValueError('VS_DIVISION must be either "Atlantic", "Central", "Northwest", "Pacific", "Southeast",'
    #                          ' "East", or "West"')
    #     individual_player_url = "http://stats.nba.com/stats/playerdashboardbyyearoveryear" \
    #                             "?DateFrom={date_from}" \
    #                             "&DateTo={date_to}" \
    #                             "&GameSegment={game_segment}" \
    #                             "&LastNGames={last_n_games}" \
    #                             "&LeagueID={league_id}" \
    #                             "&Location={location}" \
    #                             "&MeasureType={measure_type}" \
    #                             "&Month={month}" \
    #                             "&OpponentTeamID={opponent_team_id}" \
    #                             "&Outcome={outcome}" \
    #                             "&PORound={playoff_round}" \
    #                             "&PaceAdjust={pace_adjusted}" \
    #                             "&PerMode={per_type}" \
    #                             "&Period={period}" \
    #                             "&PlayerID={player_id}" \
    #                             "&PlusMinus={plus_minus}" \
    #                             "&Rank={rank}" \
    #                             "&Season={season}" \
    #                             "&SeasonSegment={season_segment}" \
    #                             "&SeasonType={season_type}" \
    #                             "&ShotClockRange={shot_clock_range}" \
    #                             "&Split={split}" \
    #                             "&VsConference={vs_conference}" \
    #                             "&VsDivision={vs_division}".format(date_from=date_from, date_to=date_to,
    #                                                                game_segment=game_segment, last_n_games=last_n_games,
    #                                                                league_id=league_id, location=location,
    #                                                                measure_type=measure_type, month=month,
    #                                                                opponent_team_id=opponent_team_id, outcome=outcome,
    #                                                                playoff_round=playoff_round,
    #                                                                pace_adjusted=pace_adjusted, per_type=per_type,
    #                                                                period=period, player_id=player_id,
    #                                                                plus_minus=plus_minus, rank=rank, season=season,
    #                                                                season_segment=season_segment,
    #                                                                season_type=season_type,
    #                                                                shot_clock_range=shot_clock_range, split=split,
    #                                                                vs_conference=vs_conference, vs_division=vs_division
    #                                                                )
    #     print(individual_player_url)
    #     headers, data = self._scrape(individual_player_url)
    #     return headers, data


    def set_players(self, league_id="00", only_current_season=0):
        print("In set_players")
        target = 'http://stats.nba.com/stats/commonallplayers?'
        params = {'IsOnlyCurrentSeason': only_current_season, 'LeagueID': league_id, 'Season': self.CURRENT_SEASON}
        headers, data = self._scrape(target=target, params=params)

        return headers, data

    def get_play_season_totals(self, player_id, league_id="00", per_mode="Totals"):
        target="https://stats.nba.com/stats/playerprofilev2?"
        params = {"LeagueID": league_id, "PerMode": per_mode, "PlayerID": player_id}
        headers, data = self._scrape(target=target, params=params)

        return headers, data

    def _scrape(self, target, params=None):
        print('In _scrape')
        try:
            r = requests.get(target, headers=self.header, params=params, timeout=10)
        except requests.exceptions.Timeout:
            raise requests.ConnectTimeout
        print(r.status_code)
        if r.status_code != 200:
            raise requests.HTTPError
        json_response = r.json()
        headers = []
        data = []
        headers.append(json_response['resultSets'][0]['headers'])
        for item in json_response['resultSets'][0]['rowSet']:
            data.append(item)
        return headers, data

    @staticmethod
    def _capitalize_word(word_string, split_on=None, split_index=None):
        if word_string and type(word_string) == str:
            if split_on:
                word_string = word_string.split(split_on)
            if split_index:
                word_string = [word_string[:split_index], word_string[split_index:]]
            for index in range(len(word_string)):
                word = [i.lower() for i in word_string[index]]
                word[0] = word[0].upper()
                word_string[index] = ''.join(word)
            join_string = '{}'.format(split_on) if split_on else ''
            return join_string.join(word_string)
        else:
            return ""

    @staticmethod
    def _get_current_season():
        today = date.today()
        year = today.year
        month = today.month
        if month < 7:
            return "{}-{}".format(year - 1, str(year)[-2:])
        else:
            return "{}-{}".format(year, str(year + 1)[-2:])


if __name__ == "__main__":
    print('test')
    scraper = NBADataScraper()
    scraper.set_players()
