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
    my_scraper = scraper.NBADataScraper()
    # headers, data = my_scraper.set_players()
    # update_players(data)
    players = models.Player.query.all()
    for player in players:
        if player.last_scraped:
            if player.inactive or player.last_scraped >= datetime.datetime.utcnow():
                pass
            else:
                print(player.get_name(), player.nba_id)
                random.seed()
                time.sleep(random.randint(3, 7))
                headers, data = my_scraper.get_play_season_totals(player.nba_id)
                for season in data:
                    nba_season = models.Season.query.filter_by(season_code=season[1]).first()
                    if not nba_season:
                        nba_season = models.Season()
                        nba_season.season_code = season[1]
                        nba_season.season_start = int(season[1].split("-")[0])
                        nba_season.season_end = nba_season.season_start + 1

                        nba_season.add_object()

                    team = models.Team.query.filter_by(nba_team_id=season[3]).first()
                    if not team:
                        team = models.Team()
                        team.nba_team_id = season[3]
                        team.team_abbr = season[4]

                        team.add_object()

                    player_season = models.PlayerSeason()
                    player_season.player_id = player.player_id
                    player_season.season_id = nba_season.season_id
                    player_season.team_id = team.team_id
                    player_season.league_id = season[2]
                    player_season.player_age = season[5]
                    player_season.games_played = season[6]
                    player_season.games_started = season[7]
                    player_season.minutes_played = season[8]
                    player_season.field_goals_made = season[9]
                    player_season.field_goals_attempted = season[10]
                    player_season.field_goal_percentage = season[11]
                    player_season.three_pointers_made = season[12]
                    player_season.three_pointers_attempted = season[13]
                    player_season.three_pointer_percentage = season[14]
                    player_season.free_throws_made = season[15]
                    player_season.free_throws_attempted = season[16]
                    player_season.free_throw_percentage = season[17]
                    player_season.offensive_rebounds = season[18]
                    player_season.defensive_rebounds = season[19]
                    player_season.total_rebounds = season[20]
                    player_season.assists = season[21]
                    player_season.steals = season[22]
                    player_season.blocks = season[23]
                    player_season.turnovers = season[24]
                    player_season.personal_fouls = season[25]
                    player_season.points = season[26]

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
