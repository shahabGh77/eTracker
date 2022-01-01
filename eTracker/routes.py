from eTracker import app, db, captcha, login_manager
from flask import request, jsonify, render_template, flash, redirect, url_for, send_file, Markup, abort
from flask_login import login_required, login_user, logout_user, current_user
from eTracker.models import User, LinkStatus
from eTracker.forms import LoginForm, RegisterForm, TrackerForm, LogoutForm
from .util import is_safe_url, logInf

import pytracking
import io

tracking_url = 'http://127.0.0.1:5000/trck/img/'


@login_manager.user_loader
def load_user(user_id):
    return User.objects(user_id=user_id).get()

@login_manager.unauthorized_handler
def unauthorized():
    return abort(404)

@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template('index.html', actNav='index')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if captcha.validate():
            email = form.email.data
            password = form.password.data
            user = User.objects(email=email).first()

            if user and user.get_password(password):
                flash(f'{user.first_name}, Yor are successfully logged in!', 'success')
                login_user(user)

                next_url = request.args.get('next')
                if not is_safe_url(next_url):
                    return abort(400)
                return redirect(next_url or url_for('index'))
            else:
                flash('wrong username or password!', 'danger')
        else:
            flash("wrong captcha", 'danger')
        return redirect(url_for('login'))
    return render_template('login.html', actNav='login', form=form, title='Login')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        return redirect(url_for('login'))
    return render_template('logout.html', actNav='logout', form=form, title='logout')

@app.route("/register", methods=['GET', 'POST'])
# @login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(user_id=User.objects.count()+1,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        flash('You are successfully registered.', 'success')
        return redirect(url_for('index'))
    if current_user.get_id() == '1':
        return render_template('register.html', actNav='register', form=form, title='Register')
    else:
        flash('You do not have access', 'danger')
        return redirect(url_for('index'))

@app.route("/trck", methods=['GET', 'POST'])
@login_required
def tracker():
    form = TrackerForm()
    if form.validate_on_submit():
        s = LinkStatus(
            sender=current_user,
            receiver = form.receiver.data,
            subject = form.subject.data,
            tags = [t for t in form.tags.data if t],
            status = {'0': logInf()}
        )
        s.save()
        open_tracking_url = pytracking.get_open_tracking_url(
            {"LID": s.link_id}, base_open_tracking_url=tracking_url,
            encryption_bytestring_key=app.config['TRACK_KEY']
        )
        flash(Markup(f"copy below link and add it as a url for an image in the body of your email:<br/> {open_tracking_url}"), 'success')
    return render_template('tracker.html', actNav='tracker', form=form, title='Tracker')

@app.route("/trck/img/<hstr>")
def img(hstr):
    full_url = tracking_url+hstr
    try:
        tracking_result = pytracking.get_open_tracking_result(
        full_url, base_open_tracking_url=tracking_url, encryption_bytestring_key=app.config['TRACK_KEY'])
    except Exception as e:
        return abort(404) 

    link_id = tracking_result.metadata.get('LID')
    s = LinkStatus.objects(link_id=link_id).get()
    seenNumber = len(s.status.keys()) + 1
    s.status[f'{seenNumber}'] = logInf()
    s.save()

    (pixel_byte_string, mime_type) = pytracking.get_open_tracking_pixel()
    return send_file(io.BytesIO(pixel_byte_string),
                     mimetype=mime_type)


@app.route('/t')
def t():
    print(current_user)
   
    return f'{current_user.get_id()}'