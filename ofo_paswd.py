#这个程序是第一次写python，
#用Python去跑一个爬虫从一个网站上面把他网站存储的共享ofo共享单车的密码循环请求出来。
#注释是后来给一位朋友写的 写的很捉急
#2017-03-19    整理时间 2018-06-19

import urllib     #这个可以去发起一个网页浏览请求
import urllib2
import re         #支持字符的重写
import MySQLdb   #支持Python和数据库的交换。

#都是引用命令 包含一些库

values = {}
num=100000     #车牌号变量              
while (num<5000000):  #循环语句  
    num= "%05d" % num         #格式转换，具体是啥别问我，再问自杀。
    values['marksId'] =num    #这好像是原网页作者定义的一个变量  我需要把我代表车牌号的num变量命名为这个然后传输给网站 
    data = urllib.urlencode(values)
    url = "http:#ofo.xwintop.com/indexAjax_getMarks"   #定义的一个变量  网址等于这个。
    request = urllib2.Request(url,data)  #像这个网址提交数据发起一个请求。
    response = urllib2.urlopen(request)  #把网址返回的数据读取  存到一个变量。
    test=response.read()   #把返回的值存到一个
    paswrd=re.findall('password":"(\d+)',test)  #正则呗  知乎找大神写的
    paswrd= "".join(list(paswrd))     #转换
    if paswrd=="":    #判断获取到的密码是否为空。
      num=int(num)
      num=num+1
    else:
      paswrd=int(paswrd)  #把密码转换为整形 
      if paswrd<999999:   #判断密码的位数 共享单车的密码不超过六位数。
        print ("ofo number:%s"%num)   #打印一下子共享单车的车牌号
        paswrd= "%04d" % paswrd   
        print paswrd                    #打印获取到的密码
        conn= MySQLdb.connect(    #开始连接数据库 下面填写的是数据库的配置,账号密码,和将要被操作的数据表。
          host='localhost',
          port = 3306,
          user='root',
          passwd='..',
          charset='utf8',
          db ='ofo',
          ) 
        cur = conn.cursor()       
        sqli="insert into test values(%s,%s)"  #把数据库操作语句写成一句变量。
        cur.execute(sqli,(num,paswrd))         #数据库语句  将值插入数据库。
        cur.close()                            
        conn.commit()                        #将所有改动行入数据库中  Python去操作数据库必须要有这个过程的。
        conn.close()                        #关闭和数据库的链接
        num=int(num)
        num=num+1
      else:
        num=int(num)
        num=num+1
        continue
print"stop"                      #循环执行完成之后 打印stop
