from datetime import datetime
from app import create_app
from app.models import db, Client, Worker, Record, Schedule, Correction
from read_json import get_data


app = create_app()


def create_db():
    db.create_all(app=app)


def delete_db():
    db.drop_all(app=app)


def save_users(users, user_class):
    for user in users:
        new_user = user_class(
            username=user['username'],
            firstname=user['firstname'],
            lastname=user['lastname'],
            sex=user['sex'],
            birthday=datetime.strptime(user['birthday'], '%d.%m.%Y').date(),
            phone=user['phone'],
            email=user['email']
            )
        if user_class == Client:
            new_user.set_password(user['password'])
        db.session.add(new_user)
        db.session.commit()


def save_records(records):
    for record in records:
        new_record = Record(
            client_id=record['client_id'],
            worker_id=record['worker_id'],
            published=datetime.strptime(record['published'], '%d.%m.%Y %H:%M:%S'),
            duration=record['duration']
        )
        new_record.set_start_time(record['start_time'])
        db.session.add(new_record)
        db.session.commit()


def save_schedules(schedules):
    for schedule in schedules:
        for time_window_schedule in range(
            int(schedule['start_time']),
            int(schedule['start_time']) + int(schedule['duration']),
            int(schedule['duration_window'])
        ):
            new_schedule = Schedule(
                worker_id=schedule['worker_id'],
                start_time=time_window_schedule,
                duration=schedule['duration_window']
            )
            new_schedule.set_week_day(time_window_schedule)
            db.session.add(new_schedule)
            db.session.commit()


def save_corrections(corrections):
    for correction in corrections:
        new_correction = Correction(
            worker_id=correction['worker_id'],
            duration=correction['duration'],
            status=correction['status']
        )
        new_correction.set_start_time(correction['start_time'])
        db.session.add(new_correction)
        db.session.commit()


def add_data():
    all_data = get_data()
    clients = all_data['clients']
    workers = all_data['workers']
    records = all_data['records']
    schedules = all_data['schedules']
    corrections = all_data['corrections']
    # administrators = all_data['administrators']
    save_users(clients, Client)
    save_users(workers, Worker)
    save_records(records)
    save_schedules(schedules)
    save_corrections(corrections)
    # save_users(administrators, Administrator)


if __name__ == "__main__":
    delete_db()
    create_db()
    with app.app_context():
        add_data()
