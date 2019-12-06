from flask.blueprints import Blueprint
from flask import render_template, views, request, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from flask_paginate import Pagination, get_page_parameter
from ext import login, db
from .model import User, Board, Article, Comment, Player, Team, Game, OneGame, game_info
from .forms import LoginForm, SignupForm, PostForm, CommentForm, SelfCenterForm, AGameForm, GameForm, TeamForm, DeleteGameForm
import config
import os
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
bp = Blueprint("front", __name__, )

@bp.route('/')
def index():
    return render_template('home.html', current_user=current_user)


@bp.route('/discussion')
def discussion():
    boards = Board.query.all()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    board_id = request.args.get('board_id', type=int, default=0)
    sort_type = request.args.get('sort', type=int, default=0)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    query_obj = Article.query

    if sort_type == 1:
        query_obj = query_obj.filter(board_id == 0 or Article.board_id == board_id).order_by(Article.register_time.desc())
        print("sort 1")
    elif sort_type == 2:
        query_obj = query_obj.filter(board_id == 0 or Article.board_id == board_id).order_by(Article.comment_num.desc())
        print("sort 2")
    else:
        query_obj = query_obj.filter(board_id == 0 or Article.board_id == board_id)

    articles = query_obj.slice(start, end)
    total = query_obj.count()
    pagination = Pagination(bs_version=3, page=page, total=total)
    return render_template('discussion.html', current_user=current_user, boards=boards,
                           articles=articles, pagination=pagination)


@bp.route('/apost', methods=['GET', 'POST'])
@login_required
def apost():
    boards = Board.query.all()
    if request.method == 'GET':
        return render_template('apost.html', current_user=current_user, boards=boards)
    else:
        form = PostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = Board.query.get(board_id)
            if not board:
                print("板块不存在")
                return redirect(url_for('front.apost'))
            post = Article(title=title, content=content, board=board, user=current_user)
            db.session.add(post)
            db.session.commit()
            print("帖子发布成功")
            return redirect(url_for('front.discussion'))
        else:
            print("帖子发布失败")
            return redirect(url_for('front.apost'))

#每个文章打开的路由
@bp.route('/article/<article_id>', methods=['GET', 'POST'])
@login_required
def article(article_id):
    now_article = Article.query.get(article_id)
    if article is None:
        return "该文章不存在"
    if request.method == 'GET':
        return render_template("article.html", article=now_article,  comments=now_article.comments)
    else:
        if not current_user.is_authenticated:
            return redirect(url_for('front.login'))
        form = CommentForm(request.form)
        if form.validate():
            content = form.content.data
            comment = Comment(content=content, article_id=article_id)
            current_user.comment_num += 1
            now_article.comment_num += 1
            comment.author = current_user
            comment.article = now_article
            db.session.add(comment)
            db.session.commit()
            print("评论成功")
            return render_template("article.html", article=now_article, comments=now_article.comments)
        else:
            print("评论失败")
            return redirect(url_for('front.article', article_id=article_id))


#战队总界面(只需要查询数据，可以添加删除数据)
@bp.route('/teams')
def teams():
    teams = Team.query.all()
    return render_template('teams.html', current_user=current_user, teams=teams)

#战队介绍界面(只需要查询数据)
@bp.route('/team/<team_id>')
def team(team_id):
    team = Team.query.get(team_id)
    if team is None:
        return "该战队不存在"
    return render_template('team.html', current_user=current_user, team=team)

# 放弃选手页面，没有什么东西
'''
@bp.route('/players')
def players():
    players = Player.query.all()
    return render_template('players.html', current_user=current_user, players=players)

#选手介绍界面(只需要查询数据，可以添加删除数据)
@bp.route('/players/<player_id>')
def player(player_id):
    player = Player.query.get(player_id)
    if player is None:
        return "该选手不存在"
    return render_template('player.html', current_user=current_user, player=player)
'''

#比赛数据(查询和修改删除数据)
@bp.route('/games')
def game():
    posts = {}
    db_games = Game.query.all()
    games = []
    for each_game in db_games:
        a_game = {}
        a_game['entity'] = each_game
        a_game['date'] = each_game.game_date
        team1 = Team.query.get(each_game.games[0].red_team_id)
        team2 = Team.query.get(each_game.games[0].blue_team_id)
        point = {}
        point[team1] = 0
        point[team2] = 0
        sm_games = []
        for sm_game in each_game.games:
            a_sm_game = {}
            winner = Team.query.get(sm_game.winner_id)
            point[winner] += 1
            red_team = Team.query.get(sm_game.red_team_id)
            blue_team = Team.query.get(sm_game.blue_team_id)
            winner = Team.query.get(sm_game.winner_id)
            a_sm_game['red_team'] = red_team
            a_sm_game['blue_team'] = blue_team
            a_sm_game['winner'] = winner
            a_sm_game['entity'] = sm_game
            sm_games.append(a_sm_game)
        a_game['team1'] = team1
        a_game['team2'] = team2
        a_game['score'] = str(point[team1]) + ":" + str(point[team2])
        a_game['desc'] = each_game.game_desc
        a_game['sm_games'] = sm_games
        games.append(a_game)
    print(games)

    return render_template('gamedata.html', current_user=current_user, games=games)



@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('front.index'))


class LoginView(views.MethodView):

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('front.index'))
        return render_template('login.html', current_user=current_user)

    def post(self):

        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password=password):
                login_user(user, remember=remember)
                return render_template('home.html', current_user=current_user)
            else:
                #用户不存在或密码错误
                return self.get()
        else:
            print(form.errors)
            return self.get()


class SignupView(views.MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('front.index'))
        return render_template('signup.html', current_user=current_user)

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password1.data
            user = User(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('front.login'))
        else:
            print(form.errors)
            return self.get()


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))

#cms views:
#个人中心
@bp.route('/selfcenter/<user_id>', methods=['GET', 'POST'])
@login_required
def selfcenter(user_id):

    if request.method == 'POST':
        if current_user.id != int(user_id):
            print(current_user.id)
            print(user_id)
            print(current_user.id != user_id)
            print("非法用户行为")
            return "非法用户行为"
        form = SelfCenterForm(request.form)
        if form.validate():
            personal_signature = form.personalized_signature.data
            name = form.username.data
            email = form.email.data
            avatar = request.files.get('header')
            filename = secure_filename(avatar.filename)
            filename = str(current_user.id) + "_" + filename
            print(filename)
            avatar.save(os.path.join(config.HEADER_UPLOAD_PATH, filename))
            img_addr = 'img/headers/' + str(filename)
            current_user.header_addr = img_addr
            current_user.personal_signature = personal_signature
            current_user.username = name
            current_user.email = email
            db.session.commit()
            return render_template('selfcenter.html', current_user=current_user)
        else:
            print("非法输入")
            print(form.errors)
            return "非法输入"
    return render_template('selfcenter.html', current_user=current_user)

@bp.route('/cms_article')
@login_required
def cms_article():
    delete_flag = request.args.get('delete', type=int, default=0)
    # 删除文章
    if delete_flag:
        delete_id = request.args.get('delete_id', type=int, default=0)
        if delete_id:
            article = Article.query.get(delete_id)
            article.board.article_num -= 1
            article.author.article_num -= 1
            db.session.delete(article)
            db.session.commit()
    my_posts = Article.query.filter_by(author_id=current_user.id)
    if current_user.admin:
        all_posts = Article.query.all()
        return render_template('cms_article.html', current_user=current_user, my_posts=my_posts, all_posts=all_posts)
    else:
        return render_template('cms_article.html', current_user=current_user, my_posts=my_posts)


@bp.route('/cms_comment')
@login_required
def cms_comment():
    delete_flag = request.args.get('delete', type=int, default=0)
    # 删除评论
    if delete_flag:
        delete_id = request.args.get('delete_id', type=int, default=0)
        if delete_id:
            comment = Comment.query.get(delete_id)
            comment.author.comment_num -= 1
            comment.article.comment_num -= 1
            db.session.delete(comment)
            db.session.commit()
    my_comments = Comment.query.filter_by(author_id=current_user.id)
    if current_user.admin:
        all_comments = Comment.query.all()
        return render_template('cms_comment.html', current_user=current_user,
                               my_comments=my_comments, all_comments=all_comments)
    else:
        return render_template('cms_comment.html', current_user=current_user, my_comments=my_comments)

@bp.route('/cms_user')
@login_required
def cms_user():
    if not current_user.admin:
        return "您没有权限访问"
    delete_flag = request.args.get('delete', type=int, default=0)
    # 删除用户
    if delete_flag:
        delete_id = request.args.get('delete_id', type=int, default=0)
        if delete_id:
            user = User.query.get(delete_id)
            for article in user.articles:
                article.board.article_num -= 1
            for comment in user.comments:
                comment.article.comment_num -= 1

            db.session.delete(user)
            db.session.commit()
    users = User.query.filter_by(admin=0)
    return render_template('cms_user.html', current_user=current_user, users=users)

@bp.route('/cms_team', methods=['GET', 'POST'])
@login_required
def cms_team():
    if not current_user.admin:
        return "您没有权限访问"
    if request.method == 'POST':
        form = TeamForm(request.form)
    else:
        delete_flag = request.args.get('delete', type=int, default=0)
        # 删除战队
        if delete_flag:
            delete_id = request.args.get('delete_id', type=int, default=0)
            if delete_id:
                team = Team.query.get(delete_id)
                db.session.delete(team)
                db.session.commit()
    teams = Team.query.all()
    return render_template('cms_team.html', current_user=current_user, teams=teams)

@bp.route('/cms_game', methods=['GET', 'POST'])
@login_required
def cms_game():
    if not current_user.admin:
        return "您没有权限访问"
    if request.method == 'POST':
        print(request.form)
        deleteForm = DeleteGameForm(request.form)
        delete_flag = request.form.get('delete')
        print(deleteForm)
        gameForm = GameForm(request.form)
        game_flag1 = request.form.get('submit1')
        print(gameForm)
        agameForm = AGameForm(request.form)
        game_flag2 = request.form.get('submit2')
        if delete_flag:
            game = Game.query.get(request.form.get('game_id'))
            print('删除比赛成功')
            db.session.delete(game)
            db.session.commit()

        elif game_flag1:
            date = request.form.get('date')
            desc = request.form.get('desc')
            if date is None or desc is None:
                return "输入错误"
            game = Game(game_desc=desc, game_date=date)
            print('添加一场比赛成功')
            db.session.add(game)
            db.session.commit()

        elif game_flag2:
            main_game = Game.query.get(request.form.get('main_game'))
            red_team = request.form.get('team1_id')
            blue_team = request.form.get('team2_id')
            mvp = Player.query.get(request.form.get('mvp'))
            red_kill = request.form.get('red_kill')
            blue_kill = request.form.get('blue_kill')
            winner_index = request.form.get('winner')
            winner = red_team
            if winner_index == 2:
                winner = blue_team
            index = request.form.get('index')
            time = request.form.get('game_time')
            one_game = OneGame(index=index, time=time, red_kill=red_kill, blue_kill=blue_kill, red_team_id=red_team,
                               blue_team_id=blue_team, winner_id=winner)
            print(type(red_team))
            one_game.red_team = red_team
            one_game.blue_team = blue_team
            one_game.winner = winner
            one_game.game = main_game
            one_game.mvp_player = mvp
            print('添加一局比赛成功')
            db.session.add(one_game)
            db.session.commit()

    games = Game.query.all()
    teams = Team.query.all()
    players = Player.query.all()
    return render_template('cms_game.html', current_user=current_user, games=games, teams=teams, players=players)