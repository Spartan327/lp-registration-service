from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from app.forms import LoginForm
from app.models import db, Client, Administrator


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
        return render_template('index.html')

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
        return render_template('login.html', page_title = title, form = login_form)
    
    @app.route('/process-login', methods = ['POST'])
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

    @app.route('/admin')
    @login_required
    def admin_index():
        
        return 'Привет админ'

    return app
