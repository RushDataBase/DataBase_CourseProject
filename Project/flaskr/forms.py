from wtforms import Form, StringField, IntegerField, DateField
from wtforms.validators import Email, InputRequired, Length, Regexp, EqualTo
from flask_ckeditor import CKEditorField

class LoginForm(Form):
    email = StringField(validators=[Email(message='请输入正确的邮箱'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()


class SignupForm(Form):
    email = StringField(validators=[Email(message='请输入正确的邮箱'), InputRequired(message='请输入邮箱')])
    username = StringField(validators=[Regexp(r"\w{2,20}", message="请输入正确格式的用户名")])
    password1 = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    password2 = StringField(validators=[EqualTo("password1", message='两次输入的密码不一致')])


class PostForm(Form):
    title = StringField(validators=[InputRequired(message='请输入标题')])
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id')])
    content = CKEditorField(validators=[InputRequired(message='请输入内容')])


class CommentForm(Form):
    content = CKEditorField(validators=[InputRequired(message='请输入内容')])

class SelfCenterForm(Form):
    personalized_signature = StringField()
    sexual = IntegerField()

class GameForm(Form):
    winner = IntegerField(validators=[InputRequired(message='请输入队伍')])
    loser = IntegerField(validators=[InputRequired(message='请输入队伍')])
    game_type = StringField(validators=[InputRequired(message='请选择比赛类型')])
    game_desc = StringField(validators=[InputRequired(message='比赛说明')])
    game_date = DateField(validators=[InputRequired(message='比赛日期')])

class AGameForm(Form):
    red_team = IntegerField(validators=[InputRequired(message='请输入红队')])
    blue_team = IntegerField(validators=[InputRequired(message='请输入蓝队')])
    winner = IntegerField(validators=[IntegerField('请选择胜利队伍')])
    red_top_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    red_jungle_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    red_mid_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    red_adc_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    red_support_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    blue_top_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    blue_jungle_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    blue_mid_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    blue_adc_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    blue_support_hero = StringField(validators=[InputRequired(message='请输入英雄')])
    game_date = DateField(validators=[InputRequired(message='请输入比赛日期')])


class TeamForm(Form):
    team_name = StringField(validators=[IntegerField(message='请输入队名')])
    team_area = StringField(validators=[InputRequired(message='请输入队伍赛区')])
    top_name = StringField(validators=[InputRequired(message='请输入上单选手')])
    jungle_name = StringField(validators=[InputRequired(message='请输入上单选手')])
    mid_name = StringField(validators=[InputRequired(message='请输入上单选手')])
    adc_name = StringField(validators=[InputRequired(message='请输入上单选手')])
    support_name = StringField(validators=[InputRequired(message='请输入上单选手')])