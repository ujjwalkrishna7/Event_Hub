import os
import secrets
from PIL import Image

from flask import render_template, url_for, flash, redirect,request, abort
from event import app, db, bcrypt,mail # type: ignore
from event.forms import RegistrationForm, LoginForm, UpdateAccountForm, EventForm,RequestResetForm,ResetPasswordForm # type: ignore
from event.models import User, Event, Registered # type: ignore
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.posted.desc()).paginate(page=page, per_page=8)    
    return render_template('home.html', event_value=events)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/approve")
def approve_admin():
    #page = request.args.get('page', 1, type=int)
    #events = Event.query.order_by(Event.posted.desc()).paginate(page=page, per_page=8)       
    events = Event.query.filter(Event.is_verified.is_(False)).all() 
    return render_template('approve_admin.html', title='Approve',event_value=events)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


def save_banner(form_banner):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_banner.filename)
    banner_fn = random_hex + f_ext
    banner_path = os.path.join(
        app.root_path, 'static/banner_pics', banner_fn)

    #output_size = (125, 125)
    i = Image.open(form_banner)
    #i.thumbnail(output_size)
    i.save(banner_path)

    return banner_fn

@app.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():        
        banner_file = save_banner(form.banner.data)                
        event = Event(name=form.name.data, description=form.description.data, author=current_user,venue = form.venue.data,date = form.date.data,time =form.time.data,max = form.max.data, banner = banner_file )
        db.session.add(event)    
        db.session.commit()
        flash('Your Event has been created, and is waiting to be Approved !', 'success')
        return redirect(url_for('home'))
    return render_template('create_event.html', title='New Event',
                           form=form, legend='Create a New Event')
                           

@app.route("/event/<int:event_id>")
def event(event_id):
    event = Event.query.get_or_404(event_id)
    no_reg = len(Registered.query.filter_by(eventId = event.id).all())
    if current_user.is_authenticated:
        register_status = Registered.query.filter_by(userId = current_user.id).all()
        x = len(register_status)
        new_list = []
        for i in range(x):
            new_list.append(register_status[i].eventId)
        event_list = []
        for i in new_list:
            event_list.append(Event.query.get_or_404(i))  
        size = len(event_list)
        eventName_list =[]
        for i in range(size):
            eventName_list.append(event_list[i].name)
        size = len(eventName_list)     

        return render_template('event.html', title=event.name, event=event, no_reg = no_reg,eventName_list =eventName_list, size=size)
    else:
        return render_template('event.html', title=event.name, event=event, no_reg = no_reg)


@app.route("/approve_event/<int:event_id>")
def event_approve(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('approve_event.html', title=event.name, event=event)    

@app.route("/approve_event/<int:event_id>/approve", methods=['POST'])
@login_required
def approving_event(event_id):
    event = Event.query.get_or_404(event_id)
    event.is_verified = True
    db.session.commit()
    flash('The event has been Approved!', 'success')
    return redirect(url_for('approve_admin'))


@app.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        db.session.commit()
        flash('Your Event has been updated!', 'success')
        return redirect(url_for('event', event_id=event.id))
    elif request.method == 'GET':
        form.name.data = event.name
        form.description.data = event.description
        form.venue.data = event.venue
        form.date.data = event.date
        form.time.data = event.time
        form.max.data = event.max

    return render_template('create_event.html', title='Update Event',
                           form=form, legend='Update your Event')    


@app.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user and current_user.is_admin == False :
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your Event has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_events(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    events = Event.query.filter_by(author=user)\
        .order_by(Event.posted.desc())\
        .paginate(page=page, per_page=8)
    return render_template('user_events.html', events=events, user=user)    


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='demo.noreply.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



@app.route("/event/<int:event_id>/register", methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    #registered_user = Registered.query.filter_by(userMail = current_user.email)
    registered = Registered(eventId=event.id,userMail = current_user.email,userId = current_user.id)
    db.session.add(registered)
    db.session.commit()
    flash('You have been registered for the event','success')
    return redirect(url_for('home'))

@app.route("/myevents")
def myevents():
    registered_event = Registered.query.filter_by(userId = current_user.id).all()
    x = len(registered_event)
    new_list = []
    for i in range(x):
        new_list.append(registered_event[i].eventId)
    event_list = []
    for i in new_list:
        event_list.append(Event.query.get_or_404(i))
    size = len(event_list)
    
    return render_template('myevent.html',event_list =event_list,size = size)    
