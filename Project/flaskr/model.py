from ext import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event


game_info = db.Table('game_info',
                    db.Column('game_id', db.Integer, db.ForeignKey('one_game.id'), primary_key=True),
                    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    register_time = db.Column(db.DateTime, default=datetime.now)
    personal_signature = db.Column(db.String(128), default="这个召唤师很懒，什么都没有留下")
    header_addr = db.Column(db.String(128), default='img/headers/default.png')

    admin = db.Column(db.Integer, default=0)
    #bbs related
    article_num = db.Column(db.Integer, default=0)
    comment_num = db.Column(db.Integer, default=0)
    articles = db.relationship('Article', backref='author', cascade='delete')
    comments = db.relationship('Comment', backref='author', cascade='delete')
    #selfcenter related

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

    def __repr__(self):
        return '<User %r>' % self.username


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    article_num = db.Column(db.Integer, default=0)
    register_time = db.Column(db.DateTime, default=datetime.now)
    articles = db.relationship('Article', backref='board', cascade='delete')

    def __init__(self, name):
        self.name = name


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comment_num = db.Column(db.Integer, default=0)
    register_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='posts', cascade='delete')

    def __init__(self, title, content, board, user):
        self.title = title
        self.content = content
        self.author = user
        self.board = board
        user.article_num += 1
        board.article_num += 1


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(256), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    register_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, content, article_id):
        self.content = content
        self.article_id = article_id


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(64), unique=True)
    logo_addr = db.Column(db.String(128), unique=True)
    team_area = db.Column(db.String(64))
    win_num = db.Column(db.Integer, default=0)
    lost_num = db.Column(db.Integer, default=0)
    s9_rank = db.Column(db.String(128))
    players = db.relationship('Player', backref='team', cascade='delete')
    '''
    red_games = db.relationship('OneGame', secondary=game_info, backref='red_team')
    blue_games = db.relationship('OneGame', secondary=game_info, backref='blue_team')
    win_games = db.relationship('OneGame', secondary=game_info, backref='winner')'''

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
    img_addr = db.Column(db.String(128), default='img/player/default.png')
    #name = db.Column(db.String(64), unique=True)
    game_name = db.Column(db.String(64), unique=True)
    #age = db.Column(db.Integer)
    #s9_total_games = db.Column(db.Integer)
    position = db.Column(db.String(64))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __init__(self, game_name, position):
        self.game_name = game_name
        self.position = position

    def add_img(self, img_addr):
        self.img_addr = img_addr


'''class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True)
    pick_times = db.Column(db.Integer)
    win_times = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name

    def add_pick_times(self):
        self.pick_times += 1

    def add_win_times(self):
        self.win_times += 1

    def get_win_rate(self):
        return self.win_times/self.pick_times'''



class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_desc = db.Column(db.String(128), nullable=False, unique=True)
    games = db.relationship('OneGame', backref='game', cascade='delete')
    game_date = db.Column(db.Date, nullable=False)

    def __init__(self, game_desc, game_date ):
        self.game_date = game_date
        self.game_desc = game_desc

class OneGame(db.Model):
    __tablename__ = 'one_game'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    index = db.Column(db.Integer)

    red_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    blue_team_id = db.Column(db.Integer,)
    winner_id = db.Column(db.Integer)
    red_kill = db.Column(db.Integer, default=0)
    blue_kill = db.Column(db.Integer, default=0)



    mvp = db.Column(db.Integer, db.ForeignKey('player.id'))
    mvp_player = db.relationship('Player', backref=db.backref('mvp_games'))
    game_time = db.Column(db.Integer, default=0)
    #MVP = db.Column(db.Integer, default=None)
    def __init__(self, index, time, red_kill, blue_kill,
                 red_team_id, blue_team_id, winner_id):
        self.index = index
        self.game_time = time
        self.red_kill = red_kill
        self.blue_kill = blue_kill
        self.red_team_id = red_team_id
        self.blue_team_id = blue_team_id
        self.winner_id = winner_id

'''
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
        self.desc = desc'''

