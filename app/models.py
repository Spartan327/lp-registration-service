from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

import enum

db = SQLAlchemy()


class RecordType(enum.Enum):
    CONFIRMED = "confimed"
    UNCONFIRMED = "unconfimed"


class CorrectionType(enum.Enum):
    DOWNTIME = "worker unavailable"
    EXTRA_HOURS = "worker available"


class Gender(enum.Enum):
    M = "male"
    F = "female"


class Client(db.Model, UserMixin):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    sex = db.Column(db.Enum(Gender), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=True, unique=True)
    records = db.relationship(
        'Record',
        backref=db.backref('client', lazy='joined'),
        lazy='dynamic'
        )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Client {self.username}>'


class Worker(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=True)
    sex = db.Column(db.Enum(Gender), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=True, unique=True)
    records = db.relationship(
        'Record',
        backref=db.backref('worker', lazy='joined'),
        lazy='dynamic'
        )
    corrections = db.relationship(
        'Correction',
        backref=db.backref('worker', lazy='joined'),
        lazy='dynamic'
        )
    schedules = db.relationship(
        'Schedule',
        backref=db.backref('worker', lazy='joined'),
        lazy='dynamic'
        )

    def __repr__(self):
        return f'<Worker {self.firstname} {self.lastname} {self.telephone}>'


class Administrator(db.Model):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=True)
    sex = db.Column(db.Enum(Gender), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=True, unique=True)

    def __repr__(self):
        return f'<Administrator {self.firstname} {self.lastname} {self.telephone}>'


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    text = db.Column(db.Text, nullable=True)
    published = db.Column(db.DateTime, nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(RecordType), nullable=True)

    def set_start_time(self, datetime_str):
        self.start_time = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M:%S')

    def __repr__(self):
        return f'<Record {self.client_id} {self.text}>'


class Correction(db.Model):
    __tablename__ = 'corrections'
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), primary_key=True, nullable=False)
    start_time = db.Column(db.TIMESTAMP, primary_key=True, nullable=False)
    status = db.Column(db.Enum(CorrectionType))
    duration = db.Column(db.Integer, nullable=False)

    def set_start_time(self, datetime_str):
        self.start_time = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M:%S')

    def get_start_time(self):
        return self.start_time.time()

    def __repr__(self):
        return f'<Correction {self.worker_id} {self.start_time} {self.status}>'


class Schedule(db.Model):
    __tablename__ = 'schedules'
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), primary_key=True, nullable=False)
    start_time = db.Column(db.Integer, primary_key=True, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    week_day = db.Column(db.Integer, nullable=False)

    def set_week_day(self, start_time):
        if 0 <= start_time < 86400:
            self.week_day = 1
        elif 86400 <= start_time < 172800:
            self.week_day = 2
        elif 172800 <= start_time < 259200:
            self.week_day = 3
        elif 259200 <= start_time < 345600:
            self.week_day = 4
        elif 345600 <= start_time < 432000:
            self.week_day = 5
        elif 432000 <= start_time < 518400:
            self.week_day = 6
        else:
            self.week_day = 7

    def get_time(self):
        return timedelta(seconds=self.start_time)

    def __repr__(self):
        return f'<Shedule {self.worker_id} {self.start_time}>'
