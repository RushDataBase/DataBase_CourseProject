from ext import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    register_time = db.Column(db.DateTime, default=datetime.now)
    power = db.Column(db.Enum('tourist, admin'), default='tourist')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_support_team(self):
        return self.support_team

    def set_power(self, power):
        self.power = power

    def __repr__(self):
        return '<User %r>' % self.username

class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    article_num = db.Column(db.Integer)
    register_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, name):
        self.name = name


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comment_num = db.Column(db.Integer, default=0)
    register_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='posts')
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship('Board', backref='posts')

    def __init__(self, title, content):
        self.title = title
        self.content = content

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref='comments')
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    article = db.relationship('Article', backref='comments')

    def __init__(self, content, article_id):
        self.content = content
        self.article_id = article_id


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(64), unique=True)
    logo_addr = db.Column(db.String(128), unique=True)
    team_area = db.Column(db.String(64), unique=True)
    win_num = db.Column(db.Integer)
    lost_num = db.Column(db.Integer)
    s9_rank = db.Column(db.String(128))

    def __init__(self, team_name, team_area):
        self.team_name = team_name
        self.team_area = team_area

    def set_logo_addr(self, logo_addr):
        self.logo_addr = logo_addr

    def set_win_num(self, num):
        self.win_num = num

    def add_win_num(self):
        self.win_num += 1

    def set_lost_num(self, num):
        self.lost_num = num

    def add_lost_num(self, num):
        self.lost_num += 1

    def update_s9_rank(self, rank):
        self.s9_rank = rank


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    game_name = db.Column(db.String(64), unique=True)
    #age = db.Column(db.Integer)
    #s9_total_games = db.Column(db.Integer)
    position = db.Column(db.Enum('Top', 'Jungle', 'Mid', 'ADC', 'Support'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', backref="players")

    def __init__(self, name, game_name, position):
        self.name = name
        self.game_name = game_name
        self.position = position

    def add_total_games(self):
        self.s9_total_games += 1


class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    pick_times = db.Column(db.Integer)
    win_times = db.Column(db.Integer)
    img_addr = db.Column(db.String(128), unique=True)

    def __init__(self, name, img_addr):
        self.name = name
        self.img_addr = img_addr

    def add_pick_times(self):
        self.pick_times += 1

    def add_win_times(self):
        self.win_times += 1

    def get_win_rate(self):
        return self.win_times/self.pick_times


game_info = db.Table('game_info',
                    db.Column('game_id', db.Integer, db.ForeignKey('one_game.id'), primary_key=True),
                    db.Column('hero_id', db.Integer, db.ForeignKey('hero.id'), primary_key=True),
)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_type = db.Column(db.Enum('BO1', 'BO3', 'BO5'), nullable=False)
    game_desc = db.Column(db.String(128), nullable=False, unique=True)
    winner = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    loser = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    game_date = db.Column(db.Date, nullable=False)
    #MVP = db.Column(db.Integer, default=None)

    def __init__(self, winner, loser, game_type, game_desc, game_date ):
        self.game_type = game_type
        self.game_date = game_date
        self.game_desc = game_desc
        self.winner = winner
        self.loser = loser


class OneGame(db.Model):
    __tablename__ = 'one_game'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    belong = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    red_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    blue_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    game = db.relationship('Game', backref=db.backref('one_games'))
    heroes = db.relationship('Hero', secondary=game_info, backref=db.backref('games'))
    winner = db.Column(db.Integer)
    loser = db.Column(db.Integer)
    #MVP = db.Column(db.Integer, default=None)
    def __init__(self, winner, game, red_team_id, blue_team_id):
        self.game = game
        self.winner = winner
        self.red_team_id = red_team_id
        self.blue_team_id = blue_team_id

class GameSchedule(db.Model):
    __tablename__ = 'gameschedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', backref=db.backref('schedulers'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', backref=db.backref('scheduler'))
    desc = db.Column(db.String(128))
    date = db.Column(db.Date)

    def __init__(self, team, date):
        self.team = team
        self.date = date

    def set_desc(self, desc):
        self.desc = desc


@event.listens_for(Comment, 'after_insert')
def receive_after_insert(mapper, connection, target):
    target.article.comment_num += 1


@event.listens_for(Article, 'after_insert')
def receive_after_insert(mapper, connection, target):
    print(connection)
    print(target.board)
    print(target)
    print(target.board.article_num)
    t = target.board.article_num
    target.board.article_num = t + 1
    print(target.board.article_num)
    target.session.commit()