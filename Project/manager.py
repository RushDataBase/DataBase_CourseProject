
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
    user = model.User(username=username, password=password, email=email)
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


if __name__ == '__main__':
    manager.run()