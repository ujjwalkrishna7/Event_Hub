from flask import render_template, url_for, flash, redirect,request, abort, Blueprint
from event import db # type: ignore
from event.events.forms import EventForm# type: ignore
from event.models import Event, Registered # type: ignore
from flask_login import  current_user,  login_required
from event.users.utils import save_banner,send_event_email,send_admin_email # type: ignore



events = Blueprint('events', __name__)

@events.route("/approve")
@login_required
def approve_admin():
    #page = request.args.get('page', 1, type=int)
    #events = Event.query.order_by(Event.posted.desc()).paginate(page=page, per_page=8)    
    if current_user.is_admin:   
        events = Event.query.filter(Event.is_verified.is_(False)).all() 
        return render_template('approve_admin.html', title='Approve',event_value=events)
    else:
        abort(403)


@events.route("/event/new", methods=['GET', 'POST'])
@login_required
def new_event():
    form = EventForm()
    if form.validate_on_submit():        
        banner_file = save_banner(form.banner.data)                
        event = Event(name=form.name.data, description=form.description.data, author=current_user,venue = form.venue.data,date = form.date.data,time =form.time.data,max = form.max.data, banner = banner_file )
        db.session.add(event)    
        db.session.commit()
        send_admin_email(event)
        flash('Your Event has been created, and is waiting to be Approved !', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_event.html', title='New Event',
                           form=form, legend='Create a New Event')
                           

@events.route("/event/<int:event_id>")
def event(event_id):
    event = Event.query.get_or_404(event_id)
    no_reg = len(Registered.query.filter_by(eventId = event.id).all())
    no_reg_confirmed = len(Registered.query.filter_by(eventId = event.id, is_coming = True).all())
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

        return render_template('event.html', title=event.name, event=event, no_reg = no_reg,eventName_list =eventName_list, size=size, no_reg_confirmed=no_reg_confirmed)
    else:
        return render_template('event.html', title=event.name, event=event, no_reg = no_reg)


@events.route("/approve_event/<int:event_id>")
@login_required
def event_approve(event_id):
    if current_user.is_admin: 
        event = Event.query.get_or_404(event_id)
        return render_template('approve_event.html', title=event.name, event=event)   
    else:
        abort(403) 

@events.route("/approve_event/<int:event_id>/approve", methods=['POST'])
@login_required
def approving_event(event_id):
    if current_user.is_admin: 
        event = Event.query.get_or_404(event_id)
        event.is_verified = True
        db.session.commit()
        flash('The event has been Approved!', 'success')
        return redirect(url_for('events.approve_admin'))
    else:
        abort(403) 


@events.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    form = EventForm()
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.venue = form.venue.data 
        event.date = form.date.data 
        event.time = form.time.data 
        event.max = form.max.data 
        event.banner = save_banner(form.banner.data) 
        db.session.commit()
        flash('Your Event has been updated!', 'success')
        return redirect(url_for('events.event', event_id=event.id))
    elif request.method == 'GET':
        form.name.data = event.name
        form.description.data = event.description
        form.venue.data = event.venue
        form.date.data = event.date
        form.time.data = event.time
        form.max.data = event.max
        
    return render_template('create_event.html', title='Update Event',
                           form=form, legend='Update your Event')    


@events.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user and current_user.is_admin == False :
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your Event has been deleted!', 'success')
    return redirect(url_for('main.home'))






@events.route("/event/<int:event_id>/register", methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    #registered_user = Registered.query.filter_by(userMail = current_user.email)
    registered = Registered(eventId=event.id,userMail = current_user.email,userId = current_user.id)
    db.session.add(registered)
    db.session.commit()
    flash('You have been registered for the event','success')
    return redirect(url_for('main.home'))


@events.route("/reg_events")
@login_required
def reg_event():
    registered_event = Registered.query.filter_by(userId = current_user.id).all()
    x = len(registered_event)
    new_list = []
    for i in range(x):
        new_list.append(registered_event[i].eventId)
    event_list = []
    for i in new_list:
        event_list.append(Event.query.get_or_404(i))
    size = len(event_list)
    
    return render_template('registered_event.html',event_list =event_list,size = size)    




@events.route("/event/<int:event_id>/confirm_event", methods=['GET', 'POST'])
@login_required
def confirm(event_id):   
    
    reg = Registered.query.filter_by(eventId=event_id).all()
    send_event_email(reg)
    flash('An email has been sent with instructions.', 'info')
    return redirect(url_for('main.home'))
    




@events.route("/confirm_event/<token>", methods=['GET', 'POST'])
def confirm_event(token):
    user = Registered.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('main.home')) 
    else:
        user.is_coming = True
        db.session.commit()
        flash('Your attendence for the event is recorded', 'success')
        return redirect(url_for('main.home'))   
