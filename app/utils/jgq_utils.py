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






def calc(zuiming, yuanpanxingqi, qishishijian, zhiri, ligong = False, zhongdaligong = False):
    jiangeqi = 1
    if yuanpanxingqi < 5:
        jiangeqi = 1
    elif yuanpanxingqi < 10 && yuanpanxingqi >5 || yuanpanxingqi = 5:
        jiangeqi = 1
    elif yuanpanxingqi == '无期':
        jiangeqi = 2
    elif yuanpanxingqi == '死缓':
        jiangeqi = 2
    return True