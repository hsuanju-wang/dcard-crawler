#!/usr/bin/env python
# coding: utf-8

# In[15]:


import argparse
import pymysql
import requests, json
h= {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
import threading
import argparse
import datetime,time
from dcard import Dcard
import json
import re


# In[16]:


# argparse
def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument("--forum", help="forum you want" ,type = str ,default="all")
    return parser.parse_args()


# In[17]:


import pymysql
def connectToDB(forum):
    db = pymysql.connect("xxx", "xxx", "xxx", charset='utf8')
    cursor = db.cursor()
    cursor.execute("use crawler_dcard_"+forum)  # 設定database
    return (cursor,db)


# In[38]:


# get post
def parse_post(post_id):
    post_url = "https://www.dcard.tw/_api/posts/%s" % (post_id)
    post_resp = requests.request("GET", post_url, headers=h)
    
    post = json.loads(post_resp.text)
    ###########################################################################################################
    ##DB中會有的欄位##
    dic= {
        "id": post['id'],
        "forumAlias" : post['forumAlias'],
        "artTitle" : post['title'],
        "artDate" : post['createdAt'],
        "artUrl" : post_url,
        "cleanResult" : post['excerpt'],
    }
    ###########################################################################################################
    return dic


# In[39]:


#用於scrapDcard() 中thread的function
def function(ID,forum):
    cursor,db = connectToDB(forum)
    result = parse_post(ID) #爬文章
    tableName = result['forumAlias']+"_"+result['artDate'][0:4]
    sql = """(id VARCHAR(255) NOT NULL,
              forumAlias VARCHAR(255) NOT NULL,
              artTitle VARCHAR(255),
              artDate datetime, 
              artUrl VARCHAR(255),
              cleanResult VARCHAR(255),
              PRIMARY KEY(id))"""
    cursor.execute("CREATE TABLE IF NOT EXISTS "+tableName+sql)
    sql2 = "INSERT INTO "+tableName + "(id,forumAlias,artTitle,artDate, artUrl,cleanResult) VALUES (%s,%s,%s,%s,%s,%s)" 
    params = (result['id'],result['forumAlias'],result['artTitle'],result['artDate'],result['artUrl'],result['cleanResult'])               
    #輸入進資料庫
    try:
       # 执行sql语句
       cursor.execute(sql2,params)
       # 执行sql语句
       db.commit()
    except:
       # 发生错误时回滚
       db.rollback()
    cursor.close
    


# In[40]:


# 爬指定時段
def scrapDcard(post_alias,startDate,endDate):
    dcard = Dcard()
    metas = dcard.forums(post_alias).get_metas(num = -1, timebound=startDate)
    threadAmount = 90
    #取出版面所有id
    listID = [result.get('id') for result in metas if result.get('createdAt')<=endDate]
    print(listID )
    
    # 用thread一次爬所有文章
    threads = []
    i = 0
    for ID in listID:  
        i+=1
        if(i%threadAmount==0):
            time.sleep(7)
        t = threading.Thread(target=function,args=[ID,post_alias])
        threads.append(t)
        t.start()
    
    # 等待所有的子執行緒結束
    for t in threads:
        t.join()


# In[18]:


def latestTime(forum): 
    cursor,db = connectToDB(forum)
    now = datetime.datetime.now()
    sql = "SELECT artDate FROM "+forum+"_"+str(now.year)+" ORDER BY artDate DESC"
    try:
        cursor.execute(sql)
    except:
        sql = "SELECT artDate FROM "+forum+"_"+str(now.year-1)+" ORDER BY artDate DESC"
        cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close
    #print(len(result))
    return result


# In[37]:


def updateToLatest(forum):
    latestArtTime = latestTime(forum)[0].strftime("%Y-%m-%d")
    nowTime = time.strftime("%Y-%m-%d", time.localtime())
    if(latestArtTime!=nowTime):
        scrapDcard(forum,latestArtTime,nowTime)


# In[ ]:


def updateAllToLatest():
    updateToLatest("nsysu")
    updateToLatest("girl")
    updateToLatest("entertainer")
    updateToLatest("funny")
    updateToLatest("mood")
    updateToLatest("trending")
    updateToLatest("rainbow")
    updateToLatest("relationship")
    updateToLatest("makeup")
    


# In[24]:


if __name__ == '__main__':
    dcard = Dcard()
    args = process_command()
    if args.forum=="all"
        updateAllToLatest()
    else:
        updateToLatest(args.forum)

