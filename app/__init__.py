from flask import Flask
from flask import render_template
from flask_bootstrap3 import Bootstrap
from .views.jgq import jgq
from .views.cbfd import cbfd
import linecache
import random
import os

app = Flask(__name__)
app.config.from_object('config')

bootstrap = Bootstrap(app)
app.register_blueprint(jgq)
app.register_blueprint(cbfd)


#from . import indexview
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    print(os.getcwd())
    basedir = os.path.abspath(os.path.dirname(__file__))
    filename = basedir +'/skill.txt'
    with open(filename) as f:
        lines = f.readlines()
        random_num = random.randint(1,len(lines))
        string = linecache.getline(filename,random_num)
    return render_template('about.html',str = string)