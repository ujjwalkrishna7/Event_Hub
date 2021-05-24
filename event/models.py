from flask import abort
from datetime import datetime
from event import db, login_manager,app, admin # type: ignore
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_admin.contrib.sqla import ModelView


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
    is_admin =  db.Column(db.Boolean, default=False)    

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
    is_verified =  db.Column(db.Boolean, default=False)

class Registered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    userMail = db.Column(db.String(100), nullable=False)
    is_coming = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.eventId},'{self.userId}','{self.userMail}')"    

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
        return Registered.query.get(user_id)
    

class Controller(ModelView):
    def is_accessible(self):
        if current_user.is_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)


class Temp(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(120),nullable = False) 
    password = db.Column(db.String(60),nullable=False)
 

    def __repr__(self):
        return f"Temp('{self.username}','{self.email}','{self.password}')" 

    def get_verification_email(self,expires_sec=1800):
        s= Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'temp_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_email(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            temp_id = s.loads(token)['temp_id']
        except:
            return None
        return Temp.query.get(temp_id)

        





admin.add_view(Controller(User, db.session))    
admin.add_view(Controller(Event, db.session)) 
admin.add_view(Controller(Registered, db.session))  
    

def __repr__(self):
    return f"Event('{self.name}', '{self.posted}')"
