from datetime import datetime, timedelta
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from app.forms import LoginForm, FilterForm, ChooseRecordForm
from app.models import db, Client, Schedule, Record, Correction
from app.date_cheker import get_current_month


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
        month = get_current_month()
        if current_user.is_authenticated:
            user_id = Client.query.filter(Client.username == current_user.username).first().id
            records_client = Record.query.filter_by(client_id=user_id).order_by(Record.start_time).all()
            return render_template('index.html', records=records_client, form=filter_form, month=month, current_date=datetime.now().date())
        return render_template('index.html', form=filter_form, month=month, current_date=datetime.now().date())

    @app.route('/check-date', methods=['GET', 'POST'])
    def check_date():
        formbtn = ChooseRecordForm()
        if request.method == 'POST':
            form = FilterForm()
            if form.validate_on_submit():
                date = request.form['date']
                date = datetime.strptime(date, '%Y-%m-%d')
                date_corrections = Correction.query.filter(Correction.start_time >= date).\
                    filter(Correction.start_time <= date + timedelta(days=1)).order_by(Correction.start_time).all()
                date_schedules = Schedule.query.filter_by(week_day=date.isoweekday()).order_by(Schedule.start_time).all()
                date_records = Record.query.filter(Record.start_time >= date).\
                    filter(Record.start_time <= date + timedelta(days=1)).order_by(Record.start_time).all()
                for date_correction in date_corrections:
                    shedule_windows_to_remove = 0
                    remove_shedule_window = None
                    for date_schedule in date_schedules:
                        # Если есть окно для удаления, то удаляем из расписания
                        if remove_shedule_window:
                            date_schedules.remove(remove_shedule_window)
                            remove_shedule_window = None
                        # Сравниваем корректировку с расписанием
                        if date_schedule.get_time() <= date_correction.get_start_time() < date_schedule.get_time_with_duration():
                            if date_correction.duration % date_schedule.duration == 0:
                                shedule_windows_to_remove = date_correction.duration / date_schedule.duration
                            else:
                                shedule_windows_to_remove = (date_correction.duration // date_schedule.duration) + 1
                        # счетчик удаления окон в расписании
                        if shedule_windows_to_remove > 0:
                            remove_shedule_window = date_schedule
                            shedule_windows_to_remove -= 1
                for date_record in date_records:
                    remove_shedule_window = None
                    for date_schedule in date_schedules:
                        if remove_shedule_window:
                            date_schedules.remove(remove_shedule_window)
                            print(remove_shedule_window.get_time())
                            remove_shedule_window = None
                        if date_schedule.get_time() == date_record.start_time.time():
                            remove_shedule_window = date_schedule
                            print(remove_shedule_window)
                    if remove_shedule_window:
                            date_schedules.remove(remove_shedule_window)
                            print(remove_shedule_window.get_time())
                            remove_shedule_window = None
                return render_template(
                    'check_date.html',
                    date_schedules=date_schedules,
                    date_corrections=date_corrections,
                    date=date,
                    date_records=date_records,
                    form=formbtn
                    )
        if request.method == 'GET':
            choose_day = request.args.get('day')
            date = datetime.strptime(choose_day, '%Y-%m-%d')
            date_corrections = Correction.query.filter(Correction.start_time >= date).\
                filter(Correction.start_time <= date + timedelta(days=1)).order_by(Correction.start_time).all()
            date_schedules = Schedule.query.filter_by(week_day=date.isoweekday()).order_by(Schedule.start_time).all()
            date_records = Record.query.filter(Record.start_time >= date).\
                filter(Record.start_time <= date + timedelta(days=1)).order_by(Record.start_time).all()
            for date_correction in date_corrections:
                shedule_windows_to_remove = 0
                remove_shedule_window = None
                for date_schedule in date_schedules:
                    # Если есть окно для удаления, то удаляем из расписания
                    if remove_shedule_window:
                        date_schedules.remove(remove_shedule_window)
                        remove_shedule_window = None
                    # Сравниваем корректировку с расписанием
                    if date_schedule.get_time() <= date_correction.get_start_time() < date_schedule.get_time_with_duration():
                        if date_correction.duration % date_schedule.duration == 0:
                            shedule_windows_to_remove = date_correction.duration / date_schedule.duration
                        else:
                            shedule_windows_to_remove = (date_correction.duration // date_schedule.duration) + 1
                    # счетчик удаления окон в расписании
                    if shedule_windows_to_remove > 0:
                        remove_shedule_window = date_schedule
                        shedule_windows_to_remove -= 1
            for date_record in date_records:
                remove_shedule_window = None
                for date_schedule in date_schedules:
                    if remove_shedule_window:
                        date_schedules.remove(remove_shedule_window)
                        print(remove_shedule_window.get_time())
                        remove_shedule_window = None
                    if date_schedule.get_time() == date_record.start_time.time():
                        remove_shedule_window = date_schedule
                        print(remove_shedule_window)
                if remove_shedule_window:
                        date_schedules.remove(remove_shedule_window)
                        print(remove_shedule_window.get_time())
                        remove_shedule_window = None
            return render_template(
                'check_date.html',
                date_schedules=date_schedules,
                date_corrections=date_corrections,
                date=date,
                date_records=date_records,
                form=formbtn
                )

    @app.route('/process-add-record', methods=['POST'])
    def process_add_record():
        form = ChooseRecordForm()
        if form.validate_on_submit():
            seconds_str = request.args.get('schedule_start_time')
            schedule_start_time = (datetime.min + timedelta(seconds=int(seconds_str))).time()
            schedule_worker = request.args.get('schedule_worker')
            date = datetime.strptime(request.args.get('date'), '%Y-%m-%d %H:%M:%S').date()
            new_record = Record(
                client_id=Client.query.filter(Client.username == current_user.username).first().id,
                worker_id=int(schedule_worker),
                published=datetime.today(),
                duration=1800,
                start_time=datetime.combine(date, schedule_start_time)
                )
            db.session.add(new_record)
            db.session.commit()
            flash('Вы успешно записались!')
            return redirect(url_for('index'))

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
        flash('Вы разлогинились')
        return redirect(url_for('index'))

    return app
