from flask.blueprints import Blueprint
from flask import render_template, views, request, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from ext import login, db
from .model import User, Board, Article, Comment, Player, Team, Game, OneGame, Hero
from .forms import LoginForm, SignupForm, PostForm, CommentForm, SelfCenterForm, AGameForm, GameForm
bp = Blueprint("front", __name__, )


@bp.route('/')
def index():
    return render_template('home.html', current_user=current_user)


@bp.route('/dicussion')
def discussion():
    boards = Board.query.all()
    articles = Article.query.all()
    return render_template('discussion.html', current_user=current_user, boards=boards, articles=articles)


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
            print(content)
            if not board:
                print("板块不存在")
                return redirect(url_for('front.apost'))
            post = Article(title=title, content=content)
            post.board = board
            post.author = current_user
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
    article = Article.query.get(article_id)
    if article is None:
        return "该文章不存在"
    if request.method == 'GET':
        return render_template("article.html", article=article)
    else:
        form = CommentForm(request.form)
        if form.validate():
            content = form.content.data
            comment = Comment(content=content, article_id=article_id)
            comment.author = current_user
            comment.article = article
            article.comments.append(comment)
            print("评论成功")
            return render_template("article.html", article=article, comments=article.comments)
        else:
            print("评论失败")
            return redirect(url_for('front.article', article_id=article_id))

#赛程(只需要查询数据)
@bp.route('/gameSchedule')
def gameSchedule():
    pass

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


#比赛数据(查询和修改删除数据)
@bp.route('/games', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.power == 'admin':
            form = GameForm(request.form)
            winner = form.winner.data
            loser = form.loser.data
            game_type = form.game_type.data
            game_desc = form.game_desc.data
            game_date = form.game_date.data
            this_game = Game(winner=winner, loser=loser, game_type=game_type,
                             game_desc=game_desc, game_date=game_date)
            db.session.add(this_game)
            db.session.commit()
    games = Game.query.all()
    return render_template('gamedata.html', current_user=current_user, games=games)

#一场bo比赛的数据
@bp.route('/agame/<game_id>', methods=['GET', 'POST'])
def agame(game_id):
    game = Game.query.get(game_id)
    if game is None:
        return "不存在该比赛"
    if request.method == 'POST':
        if current_user.is_authenticated and current_user.power == 'admin':
            form = AGameForm(request.form)
            red_team = form.red_team.data
            blue_team = form.blue_team.data
            winner = form.winner.data
            one_game = OneGame(winner, game)
            red_top_hero = Hero.query.get(form.red_top_hero.data)
            red_jungle_hero = Hero.query.get(form.red_jungle_hero.data)
            red_mid_hero = Hero.query.get(form.red_mid_hero.data)
            red_adc_hero = Hero.query.get(form.red_adc_hero.data)
            red_support_hero = Hero.query.get(form.red_support_hero.data)
            one_game.heroes.append(red_top_hero)
            one_game.heroes.append(red_jungle_hero)
            one_game.heroes.append(red_mid_hero)
            one_game.heroes.append(red_adc_hero)
            one_game.heroes.append(red_support_hero)
            blue_top_hero = Hero.query.get(form.blue_top_hero.data)
            blue_jungle_hero = Hero.query.get(form.blue_jungle_hero.data)
            blue_mid_hero = Hero.query.get(form.blue_mid_hero.data)
            blue_adc_hero = Hero.query.get(form.blue_adc_hero.data)
            blue_support_hero = Hero.query.get(form.blue_support_hero.data)
            one_game.heroes.append(blue_top_hero)
            one_game.heroes.append(blue_jungle_hero)
            one_game.heroes.append(blue_mid_hero)
            one_game.heroes.append(blue_adc_hero)
            one_game.heroes.append(blue_support_hero)
            print("添加比赛成功")
    heroes = Hero.query.all()
    return render_template('agame.html', current_user=current_user, game=game, heroes=heroes)


#个人中心
@bp.route('/selfcenter/<user_id>', methods=['GET', 'POST'])
@login_required
def selfcenter(user_id):
    if request.method == 'POST':
        if current_user.id != user_id:
            print("非法用户行为")
            return "非法用户行为"
        form = SelfCenterForm(request.form)
        if form.validate():
            personal_signature = form.personalized_signature.data
            sexual = form.sexual.data
            posts = {
                personal_signature: personal_signature, sexual: sexual,
            }
            return render_template('selfcenter.html', current_user=current_user, posts=posts)
        else:
            print("非法输入")
            return "非法输入"
    return render_template('selfcenter.html', current_user=current_user)


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
            return url_for('front.login', current_user=current_user)
        else:
            print(form.errors)
            return self.get()


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))