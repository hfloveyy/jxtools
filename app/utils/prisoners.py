#罪名、原判刑期、起始时间、上次减刑幅度、减刑起始时间

import datetime
import time

class Prisoner:
    def __init__(self, zuiming, yuanpanxingqi, chengbaodate = datetime.datetime.now(),
                 qishishijian = datetime.datetime(1900,1,1), shangcijxfd = 0,
                 jxqishishijian = datetime.datetime(1900,1,1), ligong = 0, zhongdaligong = 0):
        self.zuiming = zuiming
        self.yuanpanxingqi = yuanpanxingqi
        self.chengbaodate = chengbaodate
        self.qishishijian = qishishijian
        self.shangcijxfd = shangcijxfd
        self.jxqishishijian = jxqishishijian
        self.ligong = ligong
        self.zhongdaligong = zhongdaligong
        self.constjgq = 1
        self.flag = False

    #计算间隔时间
    def calc(self):
        #print('Prisoner')
        if self.zhongdaligong > 0:
            self.flag = True
            return self.flag
        if self.shangcijxfd > 0:
            # 比较间隔期 与上次减刑幅度
            jgq = max(self.constjgq,self.shangcijxfd)
            print(jgq)
            #计算间隔期是否已过
            if self.chengbaodate - datetime.timedelta(days=jgq*365) > self.jxqishishijian:
                self.flag = True
        else:
            if  self.chengbaodate - self.qishishijian > datetime.timedelta(days=self.constjgq*365):
                self.flag = True
        return self.flag



#无期徒刑
class WqPrisoner(Prisoner):
    def __init__(self, zuiming, yuanpanxingqi, chengbaodate=datetime.datetime.now(),
                 qishishijian=datetime.datetime(1900, 1, 1), shangcijxfd=0,
                 jxqishishijian=datetime.datetime(1900, 1, 1), ligong=0, zhongdaligong=0):
        super().__init__(zuiming, yuanpanxingqi, chengbaodate,
                         qishishijian, shangcijxfd,
                         jxqishishijian, ligong, zhongdaligong)
        self.constjgq = 2

    def calc(self):
        print('无期')
        return super().calc()




#有期徒刑
class YqPrisoner(Prisoner):
    pass



#死缓
class ShPrisoner(Prisoner):
    def __init__(self, zuiming, yuanpanxingqi, chengbaodate=datetime.datetime.now(),
                 qishishijian=datetime.datetime(1900, 1, 1), shangcijxfd=0,
                 jxqishishijian=datetime.datetime(1900, 1, 1), ligong=0, zhongdaligong=0):
        super().__init__(zuiming, yuanpanxingqi, chengbaodate,
                         qishishijian, shangcijxfd,
                         jxqishishijian, ligong, zhongdaligong)
        self.constjgq = 2
    def calc(self):
        return super().calc()


#五年以下有期徒刑
class Y5Prisoner(YqPrisoner):
    def __init__(self, zuiming, yuanpanxingqi, chengbaodate=datetime.datetime.now(),
                 qishishijian=datetime.datetime(1900, 1, 1), shangcijxfd=0,
                 jxqishishijian=datetime.datetime(1900, 1, 1), ligong=0, zhongdaligong=0):
        super().__init__(zuiming, yuanpanxingqi, chengbaodate,
                         qishishijian, shangcijxfd,
                         jxqishishijian, ligong, zhongdaligong)
        self.constjgq = 1

    def calc(self):
        return super().calc()



#五年以上十年以下有期徒刑
class Y510Prisoner(YqPrisoner):
    def __init__(self, zuiming, yuanpanxingqi, chengbaodate=datetime.datetime.now(),
                 qishishijian=datetime.datetime(1900, 1, 1), shangcijxfd=0,
                 jxqishishijian=datetime.datetime(1900, 1, 1), ligong=0, zhongdaligong=0):
        super().__init__(zuiming, yuanpanxingqi, chengbaodate,
                         qishishijian, shangcijxfd,
                         jxqishishijian, ligong, zhongdaligong)
        self.constjgq = 1

    def calc(self):
        return super().calc()




#十年以上有期徒刑
class Y10Prisoner(YqPrisoner):
    def __init__(self, zuiming, yuanpanxingqi, chengbaodate=datetime.datetime.now(),
                 qishishijian=datetime.datetime(1900, 1, 1), shangcijxfd=0,
                 jxqishishijian=datetime.datetime(1900, 1, 1), ligong=0, zhongdaligong=0):
        super().__init__(zuiming, yuanpanxingqi, chengbaodate,
                         qishishijian, shangcijxfd,
                         jxqishishijian, ligong, zhongdaligong)
        self.constjgq = 1.6

    def calc(self):
        return super().calc()


if __name__ =="__main__":
    date = datetime.datetime(2015,12,22)

    p = Y10Prisoner('杀人','10',qishishijian = date ,shangcijxfd = 0,zhongdaligong = 0)
    print(p.calc())




