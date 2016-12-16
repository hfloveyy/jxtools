from flask import Flask
from flask import render_template
from flask_bootstrap3 import Bootstrap
from .views.jgq import jgq
from .views.cbfd import cbfd



app = Flask(__name__)
app.config.from_object('config')

bootstrap = Bootstrap(app)
app.register_blueprint(jgq)
app.register_blueprint(cbfd)


#from . import indexview
@app.route('/')
def index():
    return render_template('index.html')