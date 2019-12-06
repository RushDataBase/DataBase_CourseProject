from wtforms import Form, StringField, IntegerField, DateField, FileField, SubmitField
from wtforms.validators import Email, InputRequired, Length, Regexp, EqualTo
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileRequired, FileAllowed

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
    personalized_signature = StringField(validators=[InputRequired(message='请签个名吧')])
    username = StringField(validators=[InputRequired(message='请输入用户名')])
    email = StringField(validators=[Email(message='请输入邮箱')])
    head_img = FileField(validators=[FileAllowed(['jpg','png','gif'])])


class TeamForm(Form):
    team_name = StringField(validators=[IntegerField(message='请输入队名')])
    team_area = StringField(validators=[InputRequired(message='请输入队伍赛区')])
    top_name = StringField(validators=[InputRequired(message='请输入上单选手')])
    jungle_name = StringField(validators=[InputRequired(message='请输入上单选手')])
    mid_name = StringField(validators=[InputRequired(message='请输入上单选手')])
    adc_name = StringField(validators=[InputRequired(message='请输入上单选手')])
    support_name = StringField(validators=[InputRequired(message='请输入上单选手')])


#cms game

class DeleteGameForm(Form):
    game = IntegerField(validators=[InputRequired(message='请选择比赛')])
    delete = SubmitField()


class GameForm(Form):
    game_date = DateField('date', validators=[InputRequired(message='比赛日期')])
    game_desc = StringField('desc', validators=[InputRequired(message='比赛说明')])
    addGame = SubmitField('submit1')

class AGameForm(Form):
    main_game = IntegerField(validators=[InputRequired()])
    index = IntegerField(validators=[InputRequired()])
    red_team = IntegerField(validators=[InputRequired(message='请输入红队')])
    red_kill = IntegerField(validators=[InputRequired()])
    blue_team = IntegerField(validators=[InputRequired(message='请输入蓝队')])
    blue_kill = IntegerField(validators=[InputRequired()])
    game_time = IntegerField(validators=[InputRequired()])
    mvp = IntegerField(validators=[InputRequired()])
    addOneGame = SubmitField()
