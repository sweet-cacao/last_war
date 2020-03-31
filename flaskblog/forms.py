from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
	username = StringField('ФИО',  render_kw={"placeholder": "Введите ваш ФИО"}, validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',  render_kw={"placeholder": "Введите ваш email"}, validators=[DataRequired(), Email()])
	password = PasswordField('Придумайте пароль',  render_kw={"placeholder": "Ваш пароль"}, validators=[DataRequired()])
	confirm_password = PasswordField('Подтвердите пароль',  render_kw={"placeholder": "Повторите пароль"}, validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Зарегистрироваться')

	def validate_username(self, username):

		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username is taken, please choose another one')
	
	
	def validate_email(self, email):

		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is taken, please choose another one')

class LoginForm(FlaskForm):
	email = StringField(' *Email', render_kw={"placeholder": "Введите ваш email"}, validators=[DataRequired(), Email()])
	password = PasswordField('* Пароль', render_kw={"placeholder": "Введите ваш пароль"}, validators=[DataRequired()])
	remember = BooleanField('Запомнить меня')
	submit = SubmitField('Войти')

class Search(FlaskForm):
	info = StringField('', render_kw={"placeholder": "Что собираетесь искать?"}, validators=[DataRequired()])
	submit = SubmitField('')

class UpdateAccountForm(FlaskForm):
	username = StringField('ФИО', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Загрузить фото', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Сохранить изменения')
	
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Этот email используется другим пользователем')

class PostForm(FlaskForm):
	title = StringField('Название', validators=[DataRequired()])
	content = StringField('Описание', validators=[DataRequired()])
	kategories = StringField('Категории')
	stek = StringField('Стэк технологий')
	connected_apps = StringField('Взаимосвязанные микросервисы')
	contributers = StringField('Разработчики')
	stage = StringField('Стадия')
	submit = SubmitField('Post')