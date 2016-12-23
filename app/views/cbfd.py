from flask import Blueprint, render_template

cbfd = Blueprint('cbfd', __name__, url_prefix='/cbfd')


@cbfd.route('/')
def index():
    user = 'test'
    return render_template('cbfd.html',user = user)