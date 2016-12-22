#计算服刑人员间隔期，输入罪名、起始时间、刑期止日、原判刑期
#计算方法：
#有期徒刑
#1、减刑间隔---一般-----10年以下有期徒刑---间隔时间不少于1年
#           -        10年以上有期徒刑---时间间隔不少于1年6个月
#
#           -
#           -特别-----1、减刑间隔不低于上次减刑减去的刑期
#                    2、有重大立功表现的、可以不受减刑起始时间和间隔时间限制
#无期徒刑---- 2年 （有重大立功不受限制）
#死缓        2年
#
from .prisoners import Y5Prisoner,Y10Prisoner,Y510Prisoner,WqPrisoner,ShPrisoner
import datetime,time
import xlrd


COLUMN = 9
ALLOWED_EXTENSIONS = set(['xls','xlsx'])




def format_time(time_str):
    if int(time_str) == 0:
        time_str = '19900101'
    time_str = time.strptime(time_str,'%Y%m%d')
    y, m, d = time_str[0:3]
    time_str = datetime.datetime(y, m, d)
    return time_str

def format_form(form):
    if int_date(int(form.chengbaodate.data)) or\
        int_date(int(form.qishishijian.data)) or\
        int_date(int(form.jxqishishijian.data)):
        return None
    if int(form.ligong.data) < 0 or\
        int(form.zhongdaligong.data) < 0 or\
        int(form.shangcijxfd.data) > 2:
        return None
    if '死缓' in form.yuanpanxingqi.data:
        form.yuanpanxingqi.data = -1
    if '无期' in form.yuanpanxingqi.data:
        form.yuanpanxingqi.data = 0
    return form


def calc(zuiming, yuanpanxingqi, chengbaodate = datetime.datetime.now(),
                 qishishijian = datetime.datetime(1900,1,1), shangcijxfd = 0,
                 jxqishishijian = datetime.datetime(1900,1,1), ligong = 0, zhongdaligong = 0):
    if yuanpanxingqi < 5 and yuanpanxingqi > 0:
        print("5年以下")
        p = Y5Prisoner(zuiming,yuanpanxingqi,chengbaodate,
                       qishishijian,shangcijxfd,jxqishishijian,ligong,zhongdaligong)
    elif yuanpanxingqi >5 and yuanpanxingqi <10 or yuanpanxingqi == 5:
        print('5-10年')
        p = Y510Prisoner(zuiming,yuanpanxingqi,chengbaodate,
                       qishishijian,shangcijxfd,jxqishishijian,ligong,zhongdaligong)
    elif yuanpanxingqi >10 or yuanpanxingqi == 10:
        print('10年以上')
        p = Y10Prisoner(zuiming,yuanpanxingqi,chengbaodate,
                       qishishijian,shangcijxfd,jxqishishijian,ligong,zhongdaligong)
    elif yuanpanxingqi == 0:
        print('无期徒刑')
        p = WqPrisoner(zuiming,yuanpanxingqi,chengbaodate,
                       qishishijian,shangcijxfd,jxqishishijian,ligong,zhongdaligong)
    elif yuanpanxingqi < 0:
        print('死缓')
        p = ShPrisoner(zuiming,yuanpanxingqi,chengbaodate,
                       qishishijian,shangcijxfd,jxqishishijian,ligong,zhongdaligong)

    return p.calc()

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#批量处理
def batch(filename,colnameindex=0,by_index=0):
    print(filename)
    new_list = []
    data = open_excel(filename)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    #ncols = table.ncols  # 列数
    #colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for row_num in range(1, nrows):
        row = table.row_values(row_num)
        #print(row)
        list.append(row)
    new_list = batch_jgq(list)
    return new_list

def batch_jgq(list):
    new_list = []
    for row in list:
        new_row = calc_proxy(row)
        new_list.append(new_row)
    return new_list

#检查上传文件内容是否符合模板
def is_right_file(filename,by_index = 0):
    data = open_excel(filename)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    if ncols != COLUMN:
        flag = False
    for j in range(1,nrows):
        colnames = table.row_values(j)
        for x in range(4,len(colnames)):
            if not isinstance(colnames[x],float):
                return False
    for i in range(1,nrows):
        colnames = table.row_values(i)
        if int_date(colnames[3]) or int_date(colnames[4])\
                or int_date(colnames[6]):
            return False
        if colnames[7] < 0 or colnames[8] < 0\
            or colnames[5] > 2:
            return False


    return True

#int date
def int_date(num):
    if num > 20201231 or num < 19500101 and num != 0:
        return True

#代理calc
def calc_proxy(old_list):
    list = []
    for value in old_list:
        if isinstance(value,str):
            if u'死缓' in value:
                value = -1
            elif u'无期' in value:
                value = 0
        elif value > 5 or value < 0.05:
            value = int(value)
        list.append(value)


    jgq = calc(list[1],list[2],
               int_to_datetime(list[3]),int_to_datetime(list[4]),
               list[5],
               int_to_datetime(list[6]),
               list[7],list[8])

    list.append(jgq)
    #原判刑期
    if list[2] == 0:list[2] = '无期'
    elif list[2] == -1:list[2] = '死缓'

    if list[len(list)-1] == True:list[len(list)-1] = '间隔期已过'
    else:list[len(list)-1] = '间隔期未过，不能呈报减刑'

    #立功
    if list[7] == 0:list[7] = '无'
    else:list[7] = '有'
    #重大立功
    if list[8] == 0:list[8] = '无'
    else:list[8] = '有'

    if list[6] == 0:list[6] = '未减刑'

    return list

def int_to_datetime(value):
    if value == 0.0:
        return datetime.datetime(1900, 1, 1)
    '''
    svalue = str(value)
    y = int(svalue[:4])
    m = int(svalue[4:6])
    d = int(svalue[6:])
    time = datetime.datetime(y, m, d)
    '''
    time = datetime.datetime.strptime(str(int(value)),'%Y%m%d')
    return time
#打开excel文件
def open_excel(file='file.xls'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def get_time(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


'''
if __name__ == "__main__":
    str = '19221212'
    str_time = format_time(str)
    print(str_time)
    print(type(str_time))
'''