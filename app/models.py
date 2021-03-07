from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable = False)
    lastname = db.Column(db.String(50), nullable = True)
    birthday = db.Column(db.Date, nullable = True)
    telephone = db.Column(db.String(15), nullable = False, unique = True)
    email = db.Column(db.String(150), nullable = True, unique=True)
    rool_id = db.Column(db.Integer, db.ForeignKey('rools.id'), nullable = False)
    records = db.relationship('Record', 
        backref =  db.backref('user', lazy = 'joined'), lazy = 'dynamic')

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname} {self.telephone}>'

class Rool(db.Model):
    __tablename__ = 'rools'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return f'<Rool {self.name}>'
     
class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    text = db.Column(db.Text, nullable = True)
    publish_date = db.Column(db.DateTime, nullable = False) 
    record_date = db.Column(db.DateTime, nullable = False)
    record_type_id = db.Column(db.Integer, db.ForeignKey('record_types.id'), nullable = False)

    def __repr__(self):
        return f'<Record {self.user_id} {self.text}>'

class Record_type(db.Model):
    __tablename__ = 'record_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    
    def __repr__(self):
        return f'<Record_type {self.name}>'
