from flask import Flask, render_template

from app.forms import LoginForm
from app.models import db



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

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
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title = title, form = login_form)
    return app
