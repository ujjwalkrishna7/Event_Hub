from datetime import datetime
from event import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.png')
    password = db.Column(db.String(60),nullable=False)
    event_post = db.relationship('Event',backref='author', lazy = True)

    def __repr__(self):
        return f"User('{self.username},'{self.email}','{self.image_file}')"


class Event(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(1200),nullable = False)
    posted = db.Column(db.DateTime,nullable=False,default = datetime.now())
    date = db.Column(db.DateTime,nullable=False)
    time = db.Column(db.DateTime,nullable=False)
    venue = db.Column(db.String(100),nullable = False)
    description = db.Column(db.String(2000),nullable = False)
    poster = db.Column(db.String(20),nullable=False, default = 'default.jpeg')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    

def __repr__(self):
    return f"Post('{self.name}','{self.event_posted}'"
