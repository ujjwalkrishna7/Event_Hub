![BFH Banner](https://trello-attachments.s3.amazonaws.com/542e9c6316504d5797afbfb9/542e9c6316504d5797afbfc1/39dee8d993841943b5723510ce663233/Frame_19.png)

# Event_Hub
An Event Portal for college events.  
Are u a college student who ever wanted to host their college event on a website,
where students can register for your clubs events but you're too broke to afford 
one online. Then EvenHub is the perfect freemium alternative you'll ever need.

--------------------------------------------------------------------------------------------

Web link:
https://event-hub-0.herokuapp.com

--------------------------------------------------------------------------------------------


## Team members
1. Ujjwal Krishna [https://github.com/ujjwalkrishna7/]
2. Saurav S [https://github.com/Saurav-S-Purushothaman"]
3. Rohith Nair [https://github.com/rohith-crypto]

--------------------------------------------------------------------------------------------

## Team Id
BFH/reclUvKeoTZ4h37zE/2021

--------------------------------------------------------------------------------------------

## Link to product walkthrough
[https://www.loom.com/share/498ebc1defcb48149adf99f786d0cfd2]

--------------------------------------------------------------------------------------------

## How it Works ?

GUIDE FOR GENERAL USERS:

HOW TO CREATE AN ACCOUNT?

Go on to the top right corner of the home page and click on Register. Fill in the
following details:  
Username: The username should be within 2 to 20 letters long. Also you cannot
use an existing username.  
Email: The email should be in the valid format. Also you cannot use an existing
email.  
Password:Type your password here.  
Confirm Password:Should be same as the password field.  
You will get a verification mail to your email address. Click on the link within 30
minutes to activate your account.  

HOW TO LOGIN?

Enter your email and password correctly to login. If by chance you forgot your
password, you can submit a request to reset password.

HOW TO RESET PASSWORD?

Click on forgot password on the login page. You will be directed to a new page.
Enter your email address.If your email address is valid you will get a link for
resetting password. Click on the link and enter your new password and confirm
it.

HOW TO REGISTER FOR AN EVENT?

Click on the event card on the home page to enter the event page. Click on the
register button.  
Note:Once all the slots are filled, you cannot register for an event.

HOW TO CREATE AN EVENT?

Click on the profile icon on the top right corner.Choose Add an Event. Enter the
details and upload a banner image. Your event will be listed only after the
approval of the admin.

ADMIN APPROVAL.

Your event must be approved by the admin before it can be listed in the event page.
The admin is automatically send an email to approve your event once u have submitted 
the event.  
Admin has complete control over the event listed, they can modify or remove the event
completely.

RSVP NOTIFICATION

The user who organised the event can call a RSVP Notification from their event page. They
have complete control over when to call for this notification. Once called all the users who
registered for the event are send an email to confirm their attendance. The users who 
confirmed their attendance for the event are then listed in the event page to be viewed only
by the event organiser.

--------------------------------------------------------------------------------------------

## Libraries used
Here are the Libraries used in this Project:  
astroid==2.4.2  
bcrypt==3.2.0  
blinker==1.4  
cffi==1.14.5  
click==8.0.0  
colorama==0.4.4  
dnspython==2.1.0  
email-validator==1.1.2  
Flask==2.0.0  
Flask-Admin==1.5.8  
Flask-Bcrypt==0.7.1  
Flask-Login==0.5.0  
Flask-Mail==0.9.1  
Flask-SQLAlchemy==2.5.1  
Flask-WTF==0.14.3  
greenlet==1.1.0  
gunicorn==20.1.0  
idna==3.1  
isort==5.7.0  
itsdangerous==2.0.0  
Jinja2==3.0.0  
lazy-object-proxy==1.4.3  
MarkupSafe==2.0.0  
mccabe==0.6.1  
numpy==1.19.4  
Pillow==8.2.0  
psycopg2==2.8.6  
pycparser==2.20  
pylint==2.6.0  
python-dotenv==0.17.1  
python-speech-features==0.6  
six==1.15.0  
SQLAlchemy==1.4.15  
toml==0.10.2  
Werkzeug==2.0.0  
wrapt==1.12.1  
WTForms==2.3.3  

--------------------------------------------------------------------------------------------

## How to configure
Use the config.py file in the event directory to configure the web app.

--------------------------------------------------------------------------------------------

## How to Run
Run this command "python run.py" from the root folder in terminal.

--------------------------------------------------------------------------------------------

## PACKAGE DESCRIPTION:

run.py: This is used to get the web application running  
event: This is the package containing all the modules required for the web  
application.  
errors: Used for error handling  
events:Module containing forms and routes of events  
main:Contains the main routes  
static:Contains the css and javascript file along with some images  
templates:Contains the html pages  
Users:Module containing forms and routes of events  
config.py: Contains the configurations of the web page  
models.py: Contains the classes of Users and Post  

--------------------------------------------------------------------------------------------
