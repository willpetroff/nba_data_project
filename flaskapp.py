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
    print('testing route')
    my_scraper = scraper.NBADataScraper()
    # headers, data = my_scraper.set_players()
    # update_players(data)
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
