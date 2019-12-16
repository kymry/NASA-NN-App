from flask import (Blueprint, render_template, flash, redirect)
from api.__init__ import mongo
from api.forms import MarsInquiryForm

# All views (routes) for the front end -- registered with the app via a blueprint
bp = Blueprint('front_end', __name__, url_prefix='/')  # url_prefix is appended to all URLs in this module


@bp.route('/', methods=['GET', 'POST'])
def home():

    # instantiate a new form object and accepts user input via POST
    form = MarsInquiryForm()

    if form.validate_on_submit():
        flash('Mars weather data requested for {}'.format(form.date.data))
        return redirect('/')

    # invoke the Jinja2 template engine
    return render_template('index.html', user='Kymry', form=form)


@bp.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404
