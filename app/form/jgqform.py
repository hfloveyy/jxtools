from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class JgqForm(FlaskForm):
    zuiming = StringField('name', validators=[DataRequired()])
    yuanpanxingqi = StringField('name', validators=[DataRequired()])
    chengbaodate = StringField('name', validators=[DataRequired()])
    qishishijian = StringField('name', validators=[DataRequired()])
    shangcijxfd = StringField('name', validators=[DataRequired()])
    jxqishishijian = StringField('name', validators=[DataRequired()])
    ligong = StringField('name', validators=[DataRequired()])
    zhongdaligong = StringField('name', validators=[DataRequired()])