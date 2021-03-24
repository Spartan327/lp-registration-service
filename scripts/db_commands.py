import sys
sys.path.append('../')

from datetime import datetime

from app import create_app
from app.models import db, Client, Worker, Administrator, Gender
from read_json import get_data

app=create_app()

def create_db():
    db.create_all(app=app)

def delete_db():
    db.drop_all(app=app)

def save_users(users, user_class):
    for user in users:
        new_user = user_class(
            firstname = user['firstname'], 
            lastname = user['lastname'],
            sex = user['sex'],
            birthday = datetime.strptime(user['birthday'], '%d.%m.%Y').date(),
            phone = user['phone'],
            email = user['email']
            )
        db.session.add(new_user)
        db.session.commit()

def add_data():
    all_data = get_data()
    clients = all_data['clients']
    workers = all_data['workers']
    administrators = all_data['administrators']
    save_users(clients, Client)
    save_users(workers, Worker)
    save_users(administrators, Administrator)
    
if __name__ == "__main__":
    delete_db()
    create_db()
    #with app.app_context():
    #    add_data()
