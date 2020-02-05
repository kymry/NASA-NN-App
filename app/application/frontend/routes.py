from flask import Blueprint, render_template, flash, redirect, url_for
from forms.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from models import User


# All views (routes) for the UI are registered with the app via a blueprint
bp = Blueprint('routes', __name__, url_prefix='/')


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
        return redirect(url_for('routes.login'))
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.home'))


@bp.route('/', methods=['GET', 'POST'])
def home():

    # invoke the Jinja2 template engine
    return render_template('index.html')


@bp.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
