from bs4 import BeautifulSoup
import sqlite3
from urllib import request
import re
import os
import time

def getdata(url):

    req=request.Request(url)
    req.add_header('User-Agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)')
    # req.set_proxy('http://112.193.132.182:80','http')
    data=request.urlopen(req).read()
    soup=BeautifulSoup(data,'lxml')
    

    if re.search('http://www.tripadvisor.cn/TourismBlog-t',url):
        images = soup.select('.content-image img')
        if len(images):
            
            name=re.search(r'-t\d+.html',url)
            if not os.path.exists(os.getcwd()+'/images/'+name.group()[1:-5]):
                os.makedirs(os.getcwd()+'/images/'+name.group()[1:-5])
            for image in images:

                try:
                    filename = re.search(r'-d/\S+$', image['src']).group()[3:]
                    filename = filename.replace('/', '_')
                    imgdata = request.urlopen(image['src']).read()
                    file = open(os.getcwd() + '/images/' + name.group()[1:-5] + '/' + filename, 'wb')
                    file.write(imgdata)
                    file.flush()
                    file.close()
                except Exception as a:
                    print(a)

    insert_data(conn,url,'urls')
    links=soup.select('a[href^=/TourismBlog-]')
    for link in links:
        if not select_isExist(conn,baseurl+link['href'][1:],'urls'):
            time.sleep(2)
            getdata(baseurl+link['href'][1:])

def connect_db(db_name):
    conn=sqlite3.connect(db_name)
    return conn

def close_db(conn):
    conn.close()

def create_table(conn,table_name):
    cu= conn.cursor()
    cu.execute('create table IF NOT EXISTS %s (VISITEDURL VARCHAR (255))'%table_name)
    conn.commit()

def insert_data(conn,url,table_name):
    cu=conn.cursor()
    cu.execute("INSERT INTO %s VALUES ('%s')"%(table_name,url))
    conn.commit()

def select_isExist(conn,url,table_name):
    cu=conn.cursor()
    arr=cu.execute("SELECT *FROM %s WHERE VISITEDURL='%s'"%(table_name,url))
    conn.commit()
    if len(arr.fetchall()):
        return True
    else:
        return False


conn=connect_db('visited.db')
create_table(conn,'urls')
baseurl='http://www.tripadvisor.cn/'
if not os.path.exists(os.getcwd()+'/images'):
    os.makedirs(os.getcwd() + '/images')
getdata("http://www.tripadvisor.cn/TourismBlog-g294217-Hong_Kong.html")




