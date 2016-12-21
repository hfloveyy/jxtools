from flask import Blueprint, render_template

from ..form.jgqform import JgqForm
from ..utils.jgq_utils import calc,format_time
jgq = Blueprint('jgq', __name__, url_prefix='/jgq')


@jgq.route('/', methods = ['GET', 'POST'])
def index():
    form = JgqForm()
    return render_template('jgq.html', form = form)

@jgq.route('/calc', methods = ['GET', 'POST'])
def jgq_calc():
    str = None
    flag = False
    jgq = '2年'
    form = JgqForm()
    if form.validate_on_submit():
        zuiming = form.zuiming.data
        yuanpanxingqi = int(form.yuanpanxingqi.data)
        chengbaodate = format_time(form.chengbaodate.data)
        qishishijian = format_time(form.qishishijian.data)
        shangcijxfd = int(form.shangcijxfd.data)
        jxqishishijian = format_time(form.jxqishishijian.data)
        ligong = int(form.ligong.data)
        zhongdaligong = int(form.zhongdaligong.data)

        print(zuiming,yuanpanxingqi,chengbaodate,qishishijian,shangcijxfd,
              jxqishishijian,ligong,zhongdaligong)

        flag = calc(zuiming, yuanpanxingqi, chengbaodate, qishishijian, shangcijxfd,
             jxqishishijian, ligong, zhongdaligong)
        print(flag)
        if flag:
            str = '服刑人员间隔期已过'
        else:
            str = '服刑人员间隔期未过，不能呈报减刑！'

    return render_template('jgq.html', form=form, str = str,flag = flag)
