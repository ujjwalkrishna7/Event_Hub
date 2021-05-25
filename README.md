# Event_Hub
An Event Portal for college events.

Web link:
https://event-hub-0.herokuapp.com

--------------------------------------------------------------------------------------------
GUIDE FOR GENERAL USERS:

HOW TO CREATE AN ACCOUNT?

Go on to the top right corner of the home page and click on Register. Fill in the
following details:
Username:The username should be within 2 to 20 letters long. Also you cannot
use an existing username.
Email:The email should be in the valid format. Also you cannot use an existing
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

PACKAGE DESCRIPTION:

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
