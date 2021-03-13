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

def save_items(items, MyClass):
    for item in items:
        new_item = MyClass(
            firstname = item['firstname'], 
            lastname = item['lastname'],
            sex = item['sex'],
            birthday = datetime.strptime(item['birthday'], '%d.%m.%Y').date(),
            phone = item['phone'],
            email = item['email']
            )
        db.session.add(new_item)
        db.session.commit()

def add_data():
    clients = get_data('clients')
    workers = get_data('workers')
    administrators = get_data('administrators')
    save_items(clients, Client)
    save_items(workers, Worker)
    save_items(administrators, Administrator)
    
if __name__ == "__main__":
    delete_db()
    create_db()
    with app.app_context():
        add_data()
