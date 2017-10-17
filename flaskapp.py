import datetime
import models
import os
import random
import sys
import time
import scraper

from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
models.db.init_app(app)


@app.before_request
def before_request():
    sys.stdout.flush()


@app.route('/')
def index_main():
    return "SUCCESS"


@app.route('/players/get')
def get_players():
    return jsonify(success="Players Gotten")


@app.route('/players/update')
def player_update():
    sys.stdout.flush()
    my_scraper = scraper.NBADataScraper()
    headers, data = my_scraper.set_players()
    update_players(data)
    players = models.Player.query.all()
    for player in players:
        if player.last_scraped and (not player.active or player.last_scraped >= datetime.datetime.utcnow()):
            pass
        else:
            print(player.get_name(), player.nba_id)
            random.seed()
            time.sleep(random.randint(1, 3))
            headers, data = my_scraper.get_play_season_totals(player.nba_id)
            for season in data:
                season = {i[0]: i[1] for i in zip(headers[0], season)}
                if season['TEAM_ABBREVIATION'] == 'Tot':
                    pass
                else:
                    nba_season = models.Season.query.filter_by(season_code=season['SEASON_ID']).first()
                    if not nba_season:
                        nba_season = models.Season()
                        nba_season.season_code = season['SEASON_ID']
                        nba_season.season_start = int(season['SEASON_ID'].split("-")[0])
                        nba_season.season_end = nba_season.season_start + 1

                        nba_season.add_object()

                    team = models.Team.query.filter_by(nba_team_id=season['TEAM_ID']).first()
                    if not team:
                        team = models.Team()
                        team.nba_team_id = season['TEAM_ID']
                        team.team_abbr = season['TEAM_ABBREVIATION']

                        team.add_object()
                    player_season = models.PlayerSeason.query.filter_by(player_id=player.player_id,
                                                                        season_id=nba_season.season_id,
                                                                        team_id=team.team_id).first()
                    updating_season = True
                    if not player_season:
                        player_season = models.PlayerSeason()
                        updating_season = False
                    player_season.player_id = player.player_id
                    player_season.season_id = nba_season.season_id
                    player_season.team_id = team.team_id
                    for item in season:
                        attr = player_season.get_attr_title(item)
                        if attr:
                            setattr(player_season, attr, season[item])
                    if updating_season:
                        player_season.update_object()
                    else:
                        player_season.add_object()

            player.last_scraped = datetime.datetime.utcnow()

            player.update_object()

    return "Player Seasons Gotten"


@app.route('/games/get')
def games_get():
    my_scraper = scraper.NBADataScraper()
    seasons = models.Season.query.all()
    for season in seasons:
        if season.season_start > 1995:  # Play-by-play data on NBA.com doesn't go back further than the '96-'97 season
            game_number = 0
            while game_number <= 1230:
                game = models.Game()
                # Fetch Game Info
                game_number_string = str(game_number)
                game_id = "00000"[:-len(game_number_string)] + game_number_string
                game_id = "002{season_id}{game_id}".format(str(season.season_start)[-2:], game_id)
                # Game Data
                teams = []
                game_refs = []
                players = []
                game_total_headers, game_total_data = my_scraper.get_game_boxscore(game_id, season.season_code,
                                                                                   resultSetsIndex=1)
                for team in game_total_data:
                    teams.append({i[0]: i[1] for i in zip(game_total_headers[0], team)})
                ref_headers, refs = my_scraper.get_game_misc_stats(game_id, resultSetsIndex=2)
                for ref in refs:
                    game_refs.append({i[0]: i[1] for i in zip(ref_headers[0], ref)})
                game_info_headers, game_info_data = my_scraper.get_game_misc_stats(game_id, resultSetsIndex=4)
                for game_info_row in game_info_data:
                    game_info = {i[0]: i[1] for i in zip(game_info_headers[0], game_info_row)}
                summery_headers, summery = my_scraper.get_game_misc_stats(game_id, resultSetsIndex=0)
                for summery_row in summery:
                    summery_data = {i[0]: i[1] for i in zip(summery_headers[0], summery_row)}
                new_game = models.Game()
                new_game.season_id = season.season_id
                new_game.nba_game_id = game_id
                home_team = models.Team.query.filter_by(nba_team_id=summery_data["HOME_TEAM_ID"]).first()
                new_game.home_team_id = home_team.team_id
                visiting_team = models.Team.query.filter_by(nba_team_id=summery_data["VISITOR_TEAM_ID"]).first()
                new_game.visiting_team_id = visiting_team.team_id
                for team in teams:
                    if team["TEAM_ID"] == home_team.team_id:
                        new_game.home_team_score = team["PTS"]
                    else:
                        new_game.visiting_team_score = team["PTS"]
                new_game.home_team_win = True if new_game.home_team_score > new_game.visiting_team_score else False
                new_game.periods = summery_data["LIVE_PERIOD"]
                # 2015-10-28T00:00:00
                new_game.game_date = datetime.datetime\
                    .strptime(summery_data["GAME_DATE_EST"], "%Y-%b-%dT%R:%M:%S").date()
                new_game.attendance = game_info["ATTENDANCE"]
                new_game.game_length = game_info["GAME_TIME"]

                for ref in refs:
                    ref_db = models.Ref.query.filter_by(ref_nba_id=ref["OFFICIAL_ID"]).first()
                    if not ref_db:
                        ref_db = models.Ref()
                        ref_db.ref_nba_id = ref["OFFICIAL_ID"]
                        ref_db.first_name = ref["FIRST_NAME"]
                        ref_db.last_name = ref["LAST_NAME"]

                        ref_db.add_object()
                new_game.ref_one = models.Ref.query.filter_by(ref_nba_id=refs[0]["OFFICIAL_ID"]).first().ref_id
                new_game.ref_two = models.Ref.query.filter_by(ref_nba_id=refs[1]["OFFICIAL_ID"]).first().ref_id
                new_game.ref_three = models.Ref.query.filter_by(ref_nba_id=refs[2]["OFFICIAL_ID"]).first().ref_id

                game_player_headers, game_player_data = my_scraper.get_game_boxscore(game_id, season.season_code)
                for player in game_player_data:
                    players.append({i[0]: i[1] for i in zip(game_player_headers[0], player)})

                # Play by Play Data
                headers, data = my_scraper.get_game_pbp(game_id, season.season_code)
                home_score = 0
                visitor_score = 0
                for event in data:
                    event = {i[0]: i[1] for i in zip(headers[0], event)}
                    new_event = models.GameEvent()
                    new_event.game_id = game.game_id
                    for item in event:
                        attr = new_event.get_attr_title(item)
                        if attr:
                            setattr(new_event, attr, event[item])
                    score = event["SCORE"].split('-')
                    if score:
                        home_score = int(score[1])
                        visitor_score = int(score[0])
                    new_event.home_score = home_score
                    new_event.visitor_score = visitor_score
                    new_event.score_margin = home_score - visitor_score
                    game_time = event["PCTIMESTRING"].split(':')
                    new_event.game_minutes = int(game_time[0])
                    new_event.game_seconds = int(game_time[1])
                    period = new_event.period
                    overtime_periods = 0
                    quarter_length = 12
                    if period > 4:
                        overtime_periods = period - 4
                        period = 5
                        quarter_length = 5
                    elapsed_seconds = (720 * (period - 1)) + (300 * overtime_periods) + \
                                      ((quarter_length * 60) - ((new_event.game_minutes * 60) + new_event.game_seconds))
                    new_event.game_time_elapsed_minutes = elapsed_seconds // 60
                    new_event.game_time_elapsed_seconds = elapsed_seconds % 60
                    new_event.home_event = event["HOMEDESCRIPTION"]
                    new_event.neutral_event = event["NEUTRALDESCRIPTION"]
                    new_event.visitor_event = event["VISITORDESCRIPTION"]

                    new_event.add_object()
                game_number += 1


@app.route('/game/<string:game_id>/get')
def single_game_get(game_id):
    my_scraper = scraper.NBADataScraper()
    season_code = '20162017'
    data = my_scraper.get_game_boxscore(season_code, game_id)
    print(data)

    # headers, data = my_scraper.get_game_pbp(game_id, season_code)
    # home_score = 0
    # visitor_score = 0
    # for event in data:
    #     event = {i[0]: i[1] for i in zip(headers[0], event)}
    #
    #     new_event = models.GameEvent()
    #     new_event.game_id = None
    #     for item in event:
    #         attr = new_event.get_attr_title(item)
    #         if attr:
    #             setattr(new_event, attr, event[item])
    #     score = event["SCORE"].split('-') if event["SCORE"] else None
    #     if score:
    #         home_score = int(score[1])
    #         visitor_score = int(score[0])
    #     new_event.home_score = home_score
    #     new_event.visitor_score = visitor_score
    #     new_event.score_margin = home_score - visitor_score
    #     game_time = event["PCTIMESTRING"].split(':')
    #     new_event.game_minutes = int(game_time[0])
    #     new_event.game_seconds = int(game_time[1])
    #     period = new_event.period
    #     overtime_periods = 0
    #     quarter_length = 12
    #     if period > 4:
    #         overtime_periods = period - 4
    #         period = 5
    #         quarter_length = 5
    #     elapsed_seconds = (720 * (period - 1)) + (300 * overtime_periods) + \
    #                       ((quarter_length * 60) - ((new_event.game_minutes * 60) + new_event.game_seconds))
    #     new_event.game_time_elapsed_minutes = elapsed_seconds // 60
    #     new_event.game_time_elapsed_seconds = elapsed_seconds % 60
    #     new_event.home_event = event["HOMEDESCRIPTION"]
    #     new_event.neutral_event = event["NEUTRALDESCRIPTION"]
    #     new_event.visitor_event = event["VISITORDESCRIPTION"]
    #
    #     new_event.add_object()
    # data_resp = [i for i in data]
    # return jsonify(data=data_resp)


"""
SETUP
"""


@app.route('/setup/init-db')
def init_db():
    with app.app_context():
        models.db.create_all()
    # Seed DB with initial player list
    my_scraper = scraper.NBADataScraper()
    headers, data = my_scraper.set_players()
    update_players(data)
    return "SUCCESS"


"""
Misc. Functions
"""


def update_players(data_rows):
    for player in data_rows:
        print(player[2])
        new_player = models.Player.query.filter_by(nba_id=player[0]).first()
        if new_player:
            new_player.active = player[3]
            new_player.year_end = player[5]
            new_player.games_played = True if player[12] == 'Y' else False

            new_player.update_object()
        else:
            new_player = models.Player()
            # Update to make league_id variable
            new_player.league_id = "00"
            new_player.nba_id = player[0]
            new_player.first_name = player[1].split(',')[-1].strip()
            new_player.last_name = player[1].split(',')[0].strip()
            new_player.active = player[3]
            new_player.year_start = player[4]
            new_player.year_end = player[5]
            new_player.nba_player_code = player[6]
            new_player.games_played = True if player[12] == 'Y' else False

            new_player.add_object()

    return True


if __name__ == '__main__':
    if os.name == 'nt':
        app.run(debug=True, port=3000)
    else:
        app.run()
