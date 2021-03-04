#!/usr/bin/env python
# coding: utf-8

# In[1]:

import requests, json
h= {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
import threading
import argparse
import datetime,time
from dcard import Dcard
from pymongo import MongoClient
from pycorenlp import StanfordCoreNLP
import json
import jieba
import re

# argparse
def process_command():
    parser = argparse.ArgumentParser()
    parser.add_argument("--forum", help="forum you want" ,type = str ,required=True)
    parser.add_argument("--start_date", help="start_date", type = str, required=True)
    parser.add_argument("--end_date", help="end_date" ,type = str, required=True)
    parser.add_argument("--dbURL", help="dbURL" ,type = str, default="mongodb://localhost:27017/")
    parser.add_argument("--dbName", help="dbName" ,type = str, default='31lab')
    parser.add_argument("--collectionName", help="collectionName", type = str ,default ='dcard' )
    return parser.parse_args()

###########################################################################################################
# 輸出位址
# 連 mongodb
def connectToDB(mongoURL,dbName,collectionName):
    try:
        client = MongoClient(mongoURL)
        db = client[dbName]
        collection = db[collectionName]
    except errors.ConnectionFailure as err:
        print(err)

    return collection
###########################################################################################################

# get post
def parse_post(post_id):
    post_url = "https://www.dcard.tw/_api/posts/%s" % (post_id)
    post_resp = requests.request("GET", post_url, headers=h)
    
    post = json.loads(post_resp.text)
    result = doJeiba(post['excerpt'])
    ###########################################################################################################
    ##DB中會有的欄位##
    dic= {
        "_id": post['id'],
        "forumAlias" : post['forumAlias'],
        "artTitle" : post['title'],
        "artDate" : post['createdAt'],
        "artUrl" : post_url,
        "cleanResult" : post['excerpt'],
        "result" : result,
    }
    ###########################################################################################################
    return dic

# jieba
jieba.set_dictionary('./codebase/dict.txt.big')
nlp = StanfordCoreNLP("http://127.0.0.1:9000")

# 斷詞＆標注詞性
def doJeiba (post_content):  
    
    # 先將特殊符號去掉
    # 再將連接符號以“\n”取代
    # 以“\n”切割句子
    str = re.sub("[\s+\.\/_$%^*(+\"\']+|[+——~@#￥%……&*（）]+","",post_content)
    str = re.sub("[！，。?？、,!;]+", "\n",str)
    sentences = str.split('\n')
    
    #要回傳的list
    post_result = []
    
    for sent in sentences:
        result = {"sentences":[], "tokens":[], "POS":[]}
        result['sentences'] = sent
        
        
        # 用jieba對每句話進行斷詞
        words = list(jieba.cut(sent))
        result['tokens'] = words

        # 對文章進行詞性標註
        input_sentence = ""
        input_sentence = ' '.join(result['tokens'])
        #print(input_sentence)
        
        
        output = nlp.annotate(input_sentence, properties={
            'annotators': 'tokenize,ssplit,pos',
            'tokenize.language': 'Whitespace', # first property
            'ssplit.eolonly': 'true', # second property
            'outputFormat': 'json'
        })
        try:
            pos_data = output['sentences'][0]
            temp = []
            for each_token in pos_data['tokens']:
                temp.append(each_token['word']+"#"+each_token['pos'])
        
            result['POS'] = temp
            post_result.append(result)
        except IndexError:
            pass

   
    return post_result


#用於scrapDcard() 中thread的function
def function(ID,collection):
    result = parse_post(ID) #爬文章
    collection.insert_one(result) #輸入進資料庫

# 爬指定時段
def scrapDcard(post_alias,startDate,endDate,collection):
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
            time.sleep(3)
        t = threading.Thread(target=function,args=[ID,collection])
        threads.append(t)
        t.start()
    
    # 等待所有的子執行緒結束
    for t in threads:
        t.join()

if __name__ == '__main__':
    dcard = Dcard()
    args = process_command()
    collection = connectToDB(args.dbURL,args.dbName,args.collectionName)
    scrapDcard(args.forum, args.start_date, args.end_date,collection)

