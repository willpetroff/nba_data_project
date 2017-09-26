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


class Game(BaseModel, db.Model):
    __tablename__ = "game"
    game_id = db.Column(db.Integer, primary_key=True)
    nba_game_id = db.Column(db.Integer)
    home_team = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    visiting_team = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    home_team_win = db.Column(db.Boolean)
    game_date = db.Column(db.Date)
    ref_one = db.Column(db.Integer)
    ref_two = db.Column(db.Integer)
    ref_three = db.Column(db.Integer)


class GameEvent(BaseModel, db.Model):
    __tablename__ = "game_event"
    event_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
    event_number = db.Column(db.Integer)
    message_type = db.Column(db.Integer)
    message_action_type = db.Column(db.Integer)
    period = db.Column(db.Integer)
    world_time = db.Column(db.String(5))
    game_minutes = db.Column(db.Integer)
    game_seconds = db.Column(db.Integer)
    home_event = db.Column(db.String(255))
    neutral_event = db.Column(db.String(255))
    visitor_event = db.Column(db.String(255))
    home_score = db.Column(db.Integer)
    visitor_score = db.Column(db.Integer)


    """
0	"GAME_ID"
1	"EVENTNUM"
2	"EVENTMSGTYPE"
3	"EVENTMSGACTIONTYPE"
4	"PERIOD"
5	"WCTIMESTRING"
6	"PCTIMESTRING"
7	"HOMEDESCRIPTION"
8	"NEUTRALDESCRIPTION"
9	"VISITORDESCRIPTION"
10	"SCORE"
11	"SCOREMARGIN"
12	"PERSON1TYPE"
13	"PLAYER1_ID"
14	"PLAYER1_NAME"
15	"PLAYER1_TEAM_ID"
16	"PLAYER1_TEAM_CITY"
17	"PLAYER1_TEAM_NICKNAME"
18	"PLAYER1_TEAM_ABBREVIATION"
19	"PERSON2TYPE"
20	"PLAYER2_ID"
21	"PLAYER2_NAME"
22	"PLAYER2_TEAM_ID"
23	"PLAYER2_TEAM_CITY"
24	"PLAYER2_TEAM_NICKNAME"
25	"PLAYER2_TEAM_ABBREVIATION"
26	"PERSON3TYPE"
27	"PLAYER3_ID"
28	"PLAYER3_NAME"
29	"PLAYER3_TEAM_ID"
30	"PLAYER3_TEAM_CITY"
31	"PLAYER3_TEAM_NICKNAME"
32	"PLAYER3_TEAM_ABBREVIATION"
    """



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

    def get_attr_title(self, key):
        attribute_table = {
            "PLAYER_AGE": "player_age",
            "GP": "games_played",
            "GS": "games_started",
            "MIN": "minutes_played",
            "FGM": "field_goals_made",
            "FGA": "field_goals_attempted",
            "FG_PCT": "field_goal_percentage",
            "FG3M": "three_pointers_made",
            "FG3A": "three_pointers_attempted",
            "FG3_PCT": "three_pointer_percentage",
            "FTM": "free_throws_made",
            "FTA": "free_throws_attempted",
            "FT_PCT": "free_throw_percentage",
            "OREB": "offensive_rebounds",
            "DREB": "defensive_rebounds",
            "REB": "total_rebounds",
            "AST": "assists",
            "STL": "steals",
            "BLK": "blocks",
            "TOV": "turnovers",
            "PF": "personal_fouls",
            "PTS": "points"
        }
        if key in attribute_table.keys():
            return attribute_table[key]
        else:
            return False


class Ref(BaseModel, db.Model):
    __tablename__ = "referee"
    ref_id = db.Column(db.Integer, primary_key=True)
    ref_name = db.Column(db.String(255))