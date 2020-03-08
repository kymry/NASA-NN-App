from flask import Blueprint, render_template, flash, redirect, url_for, request
from ..forms.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import User, db, SubscriptionDetails
from werkzeug.urls import url_parse


bp = Blueprint('routes', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    all_subscriptions = SubscriptionDetails.get_all_subscriptions()
    user_subscriptions = current_user.get_subscriptions()
    return render_template('user.html', user=user,
                                        user_subscriptions=user_subscriptions,
                                        all_subscriptions=all_subscriptions)


@bp.route('/subscription', methods=['GET', 'POST'])
@login_required
def subscription():
    subscription_id = int(request.form['id'])
    if current_user.is_anonymous:
        return "failure", 500
    elif current_user.is_subscribed(subscription_id):
        current_user.unsubscribe(subscription_id)
    else:
        current_user.subscribe(subscription_id)
    return "success", 200


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
        flash('Woohoo! You can now subscribe to astronomical APIs until you\'re seeing aliens!')
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
def page_not_found_error(error):
    return render_template('404.html'), 404


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@bp.route('/external/<domain>', methods=['GET'])
def external(domain):
    if domain == 'github':
        return redirect('https://github.com/kymry')
    elif domain == 'linkedin':
        return redirect('https://www.linkedin.com/in/kymryburwell/')
    else:
        redirect(url_for('routes.home'))