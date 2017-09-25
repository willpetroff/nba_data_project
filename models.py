from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseModel:
    def add_object(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        return False

    @staticmethod
    def update_object():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        return False

    def delete_object(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
        return False

    def display_attributes(self):
        for attr in sorted([i for i in self.__dict__.keys()], key=lambda x: x.lower()):
            print(attr, ':', self.__dict__[attr])

    def get_attributes(self):
        return [attr for attr in self.__dict__.keys()]

    def __return_attributes(self):
        pass


class Season(BaseModel, db.Model):
    __tablename__ = "season"
    season_id = db.Column(db.Integer, primary_key=True)
    season_code = db.Column(db.String(7))
    season_start = db.Column(db.Integer)
    season_end = db.Column(db.Integer)



class Team(BaseModel, db.Model):
    __tablename__ = "team"
    team_id = db.Column(db.Integer, primary_key=True)
    nba_team_id = db.Column(db.Integer)
    team_abbr = db.Column(db.String(5))


class Player(BaseModel, db.Model):
    __tablename__ = "player"
    player_id = db.Column(db.Integer, primary_key=True)
    nba_id = db.Column(db.Integer, unique=True)
    league_id = db.Column(db.String(2))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    active = db.Column(db.Boolean)
    year_start = db.Column(db.Integer)
    year_end = db.Column(db.Integer)
    nba_player_code = db.Column(db.String(50))
    games_played = db.Column(db.Boolean)
    last_scraped = db.Column(db.DateTime)

    def get_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class PlayerSeason(BaseModel, db.Model):
    player_season_id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    season_id = db.Column(db.Integer, db.ForeignKey('season.season_id'))
    league_id = db.Column(db.String(2))
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    player_age = db.Column(db.Integer)
    games_played = db.Column(db.Integer)
    games_started = db.Column(db.Integer)
    minutes_played = db.Column(db.Integer)
    field_goals_made = db.Column(db.Integer)
    field_goals_attempted = db.Column(db.Integer)
    field_goal_percentage = db.Column(db.Numeric(5, 3))
    three_pointers_made = db.Column(db.Integer)
    three_pointers_attempted = db.Column(db.Integer)
    three_pointer_percentage = db.Column(db.Numeric(5, 3))
    free_throws_made = db.Column(db.Integer)
    free_throws_attempted = db.Column(db.Integer)
    free_throw_percentage = db.Column(db.Numeric(5, 3))
    offensive_rebounds = db.Column(db.Integer)
    defensive_rebounds = db.Column(db.Integer)
    total_rebounds = db.Column(db.Integer)
    assists = db.Column(db.Integer)
    steals = db.Column(db.Integer)
    blocks = db.Column(db.Integer)
    turnovers = db.Column(db.Integer)
    personal_fouls = db.Column(db.Integer)
    points = db.Column(db.Integer)


    player = db.relationship('Player')
    season = db.relationship('Season')
    team = db.relationship('Team')

    def get_attr(self, key):
        attribute_table = {
            "PLAYER_AGE": self.player_age,
            "GP": self.games_played,
            "GS": self.games_started,
            "MIN": self.minutes_played,
            "FGM": self.field_goals_made,
            "FGA": self.field_goals_attempted,
            "FG_PCT": self.field_goal_percentage,
            "FG3M": self.three_pointers_made,
            "FG3A": self.three_pointers_attempted,
            "FG3_PCT": self.three_pointer_percentage,
            "FTM": self.free_throws_made,
            "FTA": self.free_throws_attempted,
            "FT_PCT": self.free_throw_percentage,
            "OREB": self.offensive_rebounds,
            "DREB": self.defensive_rebounds,
            "REB": self.total_rebounds,
            "AST": self.assists,
            "STL": self.steals,
            "BLK": self.blocks,
            "TOV": self.turnovers,
            "PF": self.personal_fouls,
            "PTS": self.points
        }
        return attribute_table[key]
#
#
# Season
#     year_start
#     year_end
#     league
#
# Team
#     city
#     name
#     season_formed
#     season_defunct
#
#     get_all_record
#     get_season_record
#     get_players
#
# Player
#     name
#     height
#     weight
#     wingspan
#     season_first
#     season_last
#
#     get_points
#     get_off_rebounds
#     get_def_rebounds
#     get_total_rebounds
#     get_assists
#     get_steals
#     get_blocks
#     get_pf
#     etc.
#
# Game
#     season
#     home_team
#     away_team
#     win_team
#     box_score_stuff
#
# PlayerGame
#     minutes_played
#     points
#     off_rebounds
#     def_rebounds
#     total_rebouns
#     assists
#     steals
#     blocks
#     fouls
#     etc.
#
# GameLineUp
#     Home 1-5
#     Away 1-5
#     minutes_played
#     points
#     off_rebounds
#     def_rebounds
#     total_rebouns
#     assists
#     steals
#     blocks
#     fouls
#     etc.
#
# PlayerSeason
#     points
#     off_rebounds
#     def_rebounds
#     total_rebouns
#     assists
#     steals
#     blocks
#     fouls
#     etc.
#
