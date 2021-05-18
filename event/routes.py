import os
import secrets
from PIL import Image

from flask import render_template, url_for, flash, redirect,request
from event import app, db, bcrypt
from event.forms import RegistrationForm, LoginForm, UpdateAccountForm
from event.models import User, Event
from flask_login import login_user, current_user, logout_user, login_required

events = [
    {
        'user': 'CET',
        'event_title': 'Dhwani',
        'content': 'CET Cultural Fest',
        'date_posted': 'May 13, 2025',
        'url': 'https://assets-global.website-files.com/5ae98eec19474e9f8c0cd052/5ae98eec19474e48570cd278_coveredited.jpg'
    },
    {
        'user': 'CET',
        'event_title': 'Dhristi',
        'content': 'CET Technical Fest',
        'date_posted': 'Jan 18 2025',
        'url': 'https://scontent.fsxv2-1.fna.fbcdn.net/v/t1.6435-9/44989850_2002772483135958_1128974446296563712_n.jpg?_nc_cat=106&ccb=1-3&_nc_sid=973b4a&_nc_ohc=9xnzeCEsFb8AX87kP2p&_nc_ht=scontent.fsxv2-1.fna&oh=97a88af0ebc51835f4b4066723f5f033&oe=60C73ED2'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', event_value=events)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


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
