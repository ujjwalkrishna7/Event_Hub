from flask import Flask,render_template,url_for,flash, redirect
from forms import RegistrationForm, LoginForm # type: ignore
from wtforms.validators import Email

app = Flask(__name__)

app.config["SECRET_KEY"] = '3e44fb9cc2dcece573e2c8451727aeb0'

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


@app.route("/register",methods=['GET','POST'])
def register():
   form = RegistrationForm()
   if form.validate_on_submit():
    flash(f'Account created for {form.username.data}!','success')
    return redirect(url_for('home'))
   return render_template("register.html",title = "Register", form = form)


@app.route("/login",methods=['GET','POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
    if form.email.data == 'admin@blog.com' and form.password.data =='password':
        flash('You have been logged in!','success')
        return redirect(url_for('home'))
    else:
        flash("Login Unsuccessful. Please check username and password",'danger')
   return render_template("login.html",title = "Login", form = form)



if __name__ == '__main__':
    app.run(debug=True)
