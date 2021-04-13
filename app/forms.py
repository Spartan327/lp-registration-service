from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Введите пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class FilterForm(FlaskForm):
    date = DateField('Выберете дату для записи', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Найти свободные записи', render_kw={"class": "btn btn-primary"})


class ChooseRecordForm(FlaskForm):
    submit = SubmitField('Записаться', render_kw={"class": "btn btn-primary"})
