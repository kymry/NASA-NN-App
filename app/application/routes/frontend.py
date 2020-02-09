from flask import Blueprint, render_template, flash, redirect, url_for, request
from forms.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from models.models import User
from models.models import db
from werkzeug.urls import url_parse


# All views (routes) for the UI are registered with the app via a blueprint
bp = Blueprint('routes', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@bp.route('/subscription', methods=['GET', 'POST'])
@login_required
def subscription():
    subscription_id = int(request.form['id'])
    if current_user.is_subscribed(subscription_id):
        current_user.unsubscribe(subscription_id)
    else:
        current_user.subscribe(subscription_id)
    print('True')
    return "success"


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Woohoo! You can now subscribe to astronomical APIs until your seeing aliens!')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('routes.login'))
        # Registers the user as logged in
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('routes.home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.home'))


@bp.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
