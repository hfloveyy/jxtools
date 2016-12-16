from flask import Blueprint, render_template

from ..form.jgqform import JgqForm

jgq = Blueprint('jgq', __name__, url_prefix='/jgq')


@jgq.route('/', methods = ['GET', 'POST'])
def index():
    form = JgqForm()
    return render_template('jgq.html', form = form)

@jgq.route('/calc', methods = ['GET', 'POST'])
def jgq_calc():
    jgq = '2年'
    form = JgqForm()
    if form.validate_on_submit():
        jgq = form.name.data

    return render_template('jgq.html', form=form, jgq=jgq)
