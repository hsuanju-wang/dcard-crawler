#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests, json
h= {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
import threading
import argparse
import datetime,time
from dcard import Dcard
import json
import re


# In[2]:


# argparse
def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument("--forum", help="forum you want" ,type = str ,default="all")
    parser.add_argument("--start_date", help="start_date", type = str, default="-1")
    parser.add_argument("--end_date", help="end_date" ,type = str, default="-1")
    return parser.parse_args()


# In[3]:


# 輸出位址
import pymysql
def connectToDB(forum):
    db = pymysql.connect("140.117.69.136", "crawler", "lab_30241#", charset='utf8')
    cursor = db.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS crawler_dcard_"+forum+" DEFAULT CHARACTER SET utf8"
    cursor.execute(sql)
    cursor.execute("use crawler_dcard_"+forum)  # 設定database
    return (cursor,db)


# In[4]:


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


# In[15]:


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
       # 執行sql
       cursor.execute(sql2,params)
       # 執行sql
       db.commit()
    except:
       # 發生錯誤回傳訊息
       db.rollback()
    cursor.close
    


# In[11]:


# 爬指定時段
def scrapDcard(post_alias,startDate,endDate):
    dcard = Dcard()
    if startDate=="-1":
        metas = dcard.forums(post_alias).get_metas(num = -1)
    else :
        metas = dcard.forums(post_alias).get_metas(num = -1, timebound=startDate)
    #取出版面所有id 
    if endDate=="-1":
        nowTime = time.strftime("%Y-%m-%d", time.localtime())
        listID = [result.get('id') for result in metas if result.get('createdAt')<=nowTime]
    else:
        listID = [result.get('id') for result in metas if result.get('createdAt')<=endDate]
       
       #print(listID )
    print(listID )
    time.sleep(10)
    threadAmount = 85
    # 用thread一次爬所有文章
    threads = []
    i = 0
    for ID in listID:  
        i+=1
        if(i%threadAmount==0):
            time.sleep(10)
        t = threading.Thread(target=function,args=[ID,post_alias])
        threads.append(t)
        t.start()
    
    # 等待所有的子執行緒結束
    for t in threads:
        t.join()
    print("Finish crawling "+ post_alias)

# In[8]:


def scrapDcardAll(startDate,endDate):
#scrapDcard("nsysu",startDate,endDate)
    scrapDcard("girl",startDate,endDate)
    #scrapDcard("entertainer",startDate,endDate)
    #scrapDcard("funny",startDate,endDate)
    #scrapDcard("mood",startDate,endDate)
    #scrapDcard("trending",startDate,endDate)
    #scrapDcard("rainbow",startDate,endDate)
    #scrapDcard("relationship",startDate,endDate)
    #scrapDcard("makeup",startDate,endDate)


# In[53]:


if __name__ == '__main__':
    args = process_command()
    if args.forum=="all":
        scrapDcardAll(args.start_date,args.end_date)
    else:
        scrapDcard(args.forum, args.start_date, args.end_date)

