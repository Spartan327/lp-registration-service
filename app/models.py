from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

class RecordType(enum.Enum):
    CONFIRMED = "confimed"
    UNCONFIRMED = "unconfimed"

class CorrectionType(enum.Enum):
    UNWORK = "unwork"
    WORK = "work"

class Gender(enum.Enum):
    M = "male"
    F = "female"

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = True)
    sex = db.Column(db.Enum(Gender), nullable = True)
    birthday = db.Column(db.Date, nullable = True)
    phone = db.Column(db.String(15), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = True, unique = True)
    records = db.relationship(
        'Record', 
        backref =  db.backref('client', lazy = 'joined'),
        lazy = 'dynamic'
        )

    def __repr__(self):
        return f'<Client {self.firstname} {self.lastname} {self.telephone}>'

class Worker(db.Model):
    __tablename__ = 'workers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = True)
    sex = db.Column(db.Enum(Gender), nullable = True)
    birthday = db.Column(db.Date, nullable = True)
    phone = db.Column(db.String(15), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = True, unique = True)
    records = db.relationship(
        'Record', 
        backref =  db.backref('worker', lazy = 'joined'),
        lazy = 'dynamic'
        )
    corrections = db.relationship(
        'Correction', 
        backref =  db.backref('worker', lazy = 'joined'),
        lazy = 'dynamic'
        )
    shedules = db.relationship(
        'Shedule', 
        backref =  db.backref('worker', lazy = 'joined'),
        lazy = 'dynamic'
        )

    def __repr__(self):
        return f'<Worker {self.firstname} {self.lastname} {self.telephone}>'

class Administrator(db.Model):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = True)
    sex = db.Column(db.Enum(Gender), nullable = True)
    birthday = db.Column(db.Date, nullable = True)
    phone = db.Column(db.String(15), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = True, unique = True)
    
    def __repr__(self):
        return f'<Administrator {self.firstname} {self.lastname} {self.telephone}>'

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable = False)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable = False)
    text = db.Column(db.Text, nullable = True)
    published = db.Column(db.DateTime, nullable = False) 
    start_time = db.Column(db.TIMESTAMP, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Enum(RecordType))

    def __repr__(self):
        return f'<Record {self.user_id} {self.text}>'

class Correction(db.Model):
    __tablename__ = 'corrections'
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), primary_key=True, nullable = False)
    start_time = db.Column(db.TIMESTAMP, primary_key=True, nullable = False)
    status = db.Column(db.Enum(CorrectionType))
    duration = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'<Correction {self.worker_id} {self.start_time} {self.status}>'

class Shedule(db.Model):
    __tablename__ = 'shedules'
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), primary_key=True, nullable = False)
    start_time = db.Column(db.Integer, primary_key=True, nullable = False)
    duration = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'<Shedule {self.worker_id} {self.start_time}>'
