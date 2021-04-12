from datetime import datetime, timedelta
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from app.forms import LoginForm, FilterForm
from app.models import db, Client, Schedule, Record, Correction


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return Client.query.get(user_id)

    @app.route('/')
    def index():
        filter_form = FilterForm()
        if current_user.is_authenticated:
            user_id = Client.query.filter(Client.username == current_user.username).first().id
            records_client = Record.query.filter_by(client_id=user_id).order_by(Record.start_time).all()
            return render_template('index.html', records=records_client, form=filter_form)
        return render_template('index.html', form=filter_form)

    @app.route('/check-date', methods=['POST'])
    def check_date():
        form = FilterForm()
        if form.validate_on_submit():
            date = request.form['date']
            date = datetime.strptime(date, '%Y-%m-%d')
            date_schedule = Schedule.query.filter_by(week_day=date.isoweekday()).order_by(Schedule.start_time).all()
            date_correction = Correction.query.filter(Correction.start_time >= date).\
                filter(Correction.start_time <= date + timedelta(days=1)).all()
            return render_template('check_date.html', date_schedule=date_schedule, date_correction=date_correction, date=date)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form, current_user=current_user)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = Client.query.filter(Client.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index'))

        flash('Неверные данные для ввода или такого пользователя не существует')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    return app
