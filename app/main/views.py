from flask import render_template, session, redirect, url_for,flash, current_app
from datetime import datetime
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email
from .. import mongo
import random
import datetime


@main.route('/rcmd')
def rcmd_page():
    topSongsList = mongo.db.sortData.find_one({'tableName' : 'topSongs'})['data']
    data = random.sample(topSongsList, 24)
    return render_template('rcmd.html', data = data)

@main.route('/')
def home_page():
    return render_template('relationship.html')    
        
    
@main.route('/sort/<value>')
def sortSongs_page(value):
    data = mongo.db.sortData.find_one({'tableName' : value})['data'][0:100]
    if value == 'topComments':
        for comment in data:
            timeStamp = str(comment['time'])[0:10]
            #print timeStamp
            comment['time'] = datetime.datetime.fromtimestamp(int(timeStamp))
    return render_template( value + '.html', data = data)
    
@main.route('/data/<value>')
def data_page(value):
    cur = mongo.db.CommentsData.find_one({'id' : value})
    return render_template( value + '.html', data = cur['data'])

@main.route('/song/<id>')
def comments_page(id):
    song_data = mongo.db.sComments.find_one({'id' : id})
    for comment in song_data['hotComments']:
        timeStamp = str(comment['time'])[0:10]
        #print timeStamp
        comment['time'] = datetime.datetime.fromtimestamp(int(timeStamp)) 
    return render_template('comments.html', data=song_data)
