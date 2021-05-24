from flask import Blueprint
from flask import render_template, url_for, flash, redirect,request
from event import db, bcrypt # type: ignore
from event.users.forms import RegistrationForm, LoginForm, UpdateAccountForm,RequestResetForm,ResetPasswordForm # type: ignore
from event.models import User, Event,Temp # type: ignore
from flask_login import login_user, current_user, logout_user, login_required
from event.users.utils import send_verification_email,save_picture,send_reset_email # type: ignore



users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()


    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        temp = Temp(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(temp)
        db.session.commit()
        temp = Temp.query.filter_by(email=form.email.data).first()
        send_verification_email(temp)
        flash('Please click on the verification link sent to your email address.', 'info')

        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))




@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_events(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    events = Event.query.filter_by(author=user)\
        .order_by(Event.posted.desc())\
        .paginate(page=page, per_page=8)
    return render_template('user_events.html', events=events, user=user)    


@users.route("/users/")
def user_event():
    page = request.args.get('page', 1, type=int)
    username = current_user.username
    user = User.query.filter_by(username=username).first_or_404()
    events = Event.query.filter_by(author=user)\
        .order_by(Event.posted.desc())\
        .paginate(page=page, per_page=8)
    return render_template('my_events.html', events=events, user=user)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)






@users.route("/register/<token>", methods=['GET', 'POST'])
def resett_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    temp = Temp.verify_email(token)
    if temp is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.register'))

    if temp:
        check_user=User.query.filter_by(username=temp.username).all()
        if len(check_user)>0:
            Temp.query.filter_by(username=temp.username).delete()
            db.session.commit()
            flash('Username has already been taken','warning')
            return redirect(url_for('users.register'))
        user = User(username=temp.username, email=temp.email, password=temp.password)
        db.session.add(user)
        Temp.query.filter_by(email=temp.email).delete()
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
