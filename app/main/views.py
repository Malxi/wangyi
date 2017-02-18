from flask import render_template, session, redirect, url_for,flash, current_app
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email
from .. import mongo
import random

'''
@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['know'] = False
            if current_app.config['FLASK_ADMIN']:
                send_email(current_app.config['FLASK_ADMIN'], 'New user', 'mail/new_user', user=user)
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form,name=session.get('name'), known=session.get('know', False), current_time=datetime.utcnow())
'''

@main.route('/')
def home_page():
    topSongsList = mongo.db.topSongs.find_one()['topSongs']
    data = random.sample(topSongsList, 24)
    return render_template('rcmd.html', data = data)

@main.route('/data/<value>')
def data_page(value):
    cur = mongo.db.CommentsData.find_one({'id' : value})
    return render_template( value + '.html', data = cur['data'])

@main.route('/song/<id>')
def comments_page(id):
    song_data = mongo.db.comments.find_one({'id' : id})
    return render_template('comments.html', data=song_data)
       
'''
@main.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@main.route('/config')
def test():
    return str(current_app.config['FLASK_ADMIN'])
'''
