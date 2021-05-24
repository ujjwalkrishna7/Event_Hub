from flask import render_template,request, Blueprint
from event.models import Event # type: ignore

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    events = Event.query.filter_by(is_verified = True).order_by(Event.date.desc()).paginate(page=page, per_page=8)    
    return render_template('home.html', event_value=events)


@main.route("/about")
def about():
    return render_template('about.html', title='About')

