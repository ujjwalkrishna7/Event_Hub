import os
import secrets
from PIL import Image
from flask import url_for,request,current_app
from event import mail # type: ignore
from flask_mail import Message



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='demo.noreply.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_admin_email(event):
    msg = Message('New Events are waiting to be Approved',
                  sender='demo.noreply.com',
                  recipients=['eventhubofficial0@gmail.com'])
    msg.body = f'''Event:
{event.name}
Description:
{event.description}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



def send_event_email(user):
    x = len(user)
    for i in range(x):
        token = user[i].get_reset_token()
        msg = Message('Are u coming for the Registered Event',
                    sender='demo.noreply.com',
                    recipients=[user[i].userMail])
        msg.body = f'''If you are coming for the event, please confirm here:
{url_for('events.confirm_event', token=token, _external=True)}

'''
        mail.send(msg)


def send_verification_email(temp):
    token = temp.get_verification_email()
    msg = Message('Verify your email.',
                  sender='noreply@demo.com',
                  recipients=[temp.email])
    msg.body = f'''To verify your email, visit the following link:
{url_for('users.resett_token', token=token, _external=True)}

If you did not initiate the verification,please ignore.
'''
    mail.send(msg)



def save_banner(form_banner):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_banner.filename)
    banner_fn = random_hex + f_ext
    banner_path = os.path.join(
        current_app.root_path, 'static/banner_pics', banner_fn)

    #output_size = (125, 125)
    i = Image.open(form_banner)
    #i.thumbnail(output_size)
    i.save(banner_path)

    return banner_fn