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


def format_time(time_str):
    if int(time_str) == 0:
        time_str = '19900101'
    time_str = time.strptime(time_str,'%Y%m%d')
    y, m, d = time_str[0:3]
    time_str = datetime.datetime(y, m, d)
    return time_str



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


'''
if __name__ == "__main__":
    str = '19221212'
    str_time = format_time(str)
    print(str_time)
    print(type(str_time))
'''