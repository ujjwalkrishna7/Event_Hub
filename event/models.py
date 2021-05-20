from datetime import datetime
from event import db, login_manager,app # type: ignore
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Event(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(1200),nullable = False)
    posted = db.Column(db.DateTime,nullable=False,default = datetime.now())
    date = db.Column(db.Date,nullable=True)
    time = db.Column(db.Time,nullable=True)
    venue = db.Column(db.String(100),nullable = True)
    description = db.Column(db.String(2000),nullable = False)
    banner = db.Column(db.String(20),nullable=True,default='default.png')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable = False)
    max = db.Column(db.Integer,nullable =True)


class Registered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False,unique=True)
    userMail = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.eventId},'{self.userId}','{self.userMail}')"
        



def __repr__(self):
    return f"Event('{self.name}', '{self.posted}')"
