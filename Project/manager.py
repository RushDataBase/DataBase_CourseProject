
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from lolWeb import create_app
from ext import db
from flaskr import model


app = create_app()
manager = Manager(app)


Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    for i in range(100):
        user = model.User(username=str(i), password='123456', email=str(i) + 'gfff@qq.com')
        db.session.add(user)
        db.session.commit()
    print("cms add user successfully")

@manager.option('-i', '--id', dest='id')
@manager.option('-a', '--admin', dest='admin')
def set_user_admin(id, admin):
    user = model.User.query.get(id)
    user.admin = admin
    db.session.commit()

@manager.option('-i', '--id', dest='id')
def delete_board(id):
    board = model.Board.query.get(id)
    db.session.delete(board)
    db.session.commit()



@manager.option('-t', '--team_name', dest='team_name')
@manager.option('-a', '--team_area', dest='team_area')
def create_team(team_name, team_area):
    team = model.Team(team_name=team_name, team_area=team_area)
    db.session.add(team)
    db.session.commit()
    print("common add team successfully")

@manager.option('-n', '--name', dest='name')
def create_board(name):
    board = model.Board(name=name)
    db.session.add(board)
    db.session.commit()

@manager.option('-f', '--file', dest='file')
def import_players(file):
    with open(file, 'r') as f:
        for j in range(8):
            info = f.readline()
            if info is None:
                break
            team = info.split(':')[-1]
            team = team.strip()
            team = model.Team.query.filter_by(team_name=team.upper()).first()
            print(team)
            for i in range(5):
                player_info = f.readline()
                player_infos = player_info.split(',')
                player_name = player_infos[0].strip()
                player_position = player_infos[1].strip()
                player = model.Player(player_name, player_position)
                player.team = team
                addr = ('img/player/' + player_name + '.png')
                player.add_img(addr)
                print(player_name + ":" + player_position)
                db.session.add(player)
                db.session.commit()
            print('++++++++++++++++++++++')

@manager.option('-f', '--file', dest='file')
def import_teams(file):
    with open(file, 'r') as f:
        for i in range(8):
            info = f.readline()
            team_info = info.split(',')
            team_name = team_info[0].strip()
            team_area = team_info[1].strip()
            team = model.Team(team_name=team_name, team_area=team_area)
            addr = ('img/logo/' + team_name.lower() + '.png')
            team.set_logo_addr(addr)
            print(team_name + ', ' + team_area + ', ' + addr)
            db.session.add(team)
            db.session.commit()


if __name__ == '__main__':
    manager.run()