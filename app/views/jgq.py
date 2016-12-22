from flask import Blueprint, render_template, make_response, send_file, request, jsonify
from werkzeug.utils import secure_filename
import os
import time
import base64

from ..form.jgqform import JgqForm
from ..utils.jgq_utils import calc,format_time, allowed_file, batch, is_right_file, get_time, format_form
import flask_excel as excel
import copy


jgq = Blueprint('jgq', __name__, url_prefix='/jgq')






export_data = []
data_flag = False


@jgq.route('/', methods = ['GET', 'POST'])
def index():
    form = JgqForm()
    return render_template('jgq.html', form = form)


#计算间隔期
@jgq.route('/calc', methods = ['GET', 'POST'])
def jgq_calc():
    str = None
    flag = False
    jgq = '2年'
    form = JgqForm()
    if form.validate_on_submit():
        form = format_form(form)
        if form:
            zuiming = form.zuiming.data
            yuanpanxingqi = int(form.yuanpanxingqi.data)
            chengbaodate = format_time(form.chengbaodate.data)
            qishishijian = format_time(form.qishishijian.data)
            shangcijxfd = int(form.shangcijxfd.data)
            jxqishishijian = format_time(form.jxqishishijian.data)
            ligong = int(form.ligong.data)
            zhongdaligong = int(form.zhongdaligong.data)

        #print(zuiming,yuanpanxingqi,chengbaodate,qishishijian,shangcijxfd,
        #      jxqishishijian,ligong,zhongdaligong)

            flag = calc(zuiming, yuanpanxingqi, chengbaodate, qishishijian, shangcijxfd,
             jxqishishijian, ligong, zhongdaligong)
        #print(flag)
            if flag:
                str = '服刑人员间隔期已过'
            else:
                str = '服刑人员间隔期未过，不能呈报减刑！'

            return render_template('jgq.html', form=form, str = str,flag = flag)
        else:
            form = JgqForm()
            flag = False
            str = '输入信息有误，请检查！'
            return render_template('jgq.html', form=form, str=str, flag=flag)


#下载模板
@jgq.route('/down_template',methods = ['GET'])
def download_template():
    filename = 'template.xls'
    response = make_response(send_file(filename))
    response.headers["Content-Disposition"] = "attachment; filename={0};".format(filename)
    return response

#下载批量计算后的文件
@jgq.route('/download_jgq',methods = ['GET'])
def download_jgq():
    global data_flag
    if data_flag:
        time_name = 'jian_ge_qi_'+get_time(time.time())
        #data_flag = False
        return excel.make_response_from_array(export_data, file_type="xls",file_name = time_name)
    else:
        file_str = '文件未上传，请上传文件！'
        data_flag = False
        return render_template('batch.html', str=file_str)



# 上传文件
@jgq.route('/api/upload', methods=['POST'], strict_slashes=False)
def api_upload():
    global export_data
    global data_flag
    file_str = '文件上传不成功，请重新上传！'

    file_upload = False
    form = JgqForm()
    file_dir = 'upload'
    template_name = 'batch'
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir, 'upload')
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        token = base64.b64encode(new_filename.encode('ascii'))
        #f.save(os.path.join(file_dir, template_name))  # 保存文件到upload目录

        #print(token)
        file_str = '文件上传成功！'
        if is_right_file(file_dir+'/'+new_filename):
            file_upload = True
            data = batch(file_dir+'/'+new_filename)
            export_data = data
            data_flag = True
        else:
            file_str = '服刑人员信息填写不全或有误，请认真填写后上传！'
            data_flag = False
            data = []
        return render_template('batch.html', fileupload = file_upload, str = file_str,data = data)
        #return jsonify({"errno": 0, "errmsg": "上传成功", "token": str(token)})
    else:
        return render_template('batch.html', fileupload = file_upload, str = file_str)
        #return jsonify({"errno": 1001, "errmsg": "上传失败"})



