
# Dcard_mongodb

Dcard 網頁資料爬蟲程式，爬完後將資料存於mongodb。

## 使用方式

**scrapDcard(post_alias,startDate,endDate)：** 此函式用來實現爬蟲功能，於函式內依要求格式輸入指定的版，指定的日期區間，即可爬取該日期區間內該版的所有文章。 scrapDcard中包含三個參數：
   * post_alias : 預爬取資料之看板名稱，要求型態為字串,此參數是必要的。
  * startDate : 爬取之資料的起始日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，此參數是必要的。
  * endDate : 爬取之資料的結束日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，此參數是必要的。
  * collection : 資料集，connectToDB（）的回傳值。

<br>

**connectToDB(mongoURL,dbName,collectionName)：** 此函式用來連接mongodb，為其輸出欄位包括文章編號(_id)、看板名稱(forumAlias)、標題(artTitle)、日期(artDate)、網址(artUrl)、純文字結果(cleanResult)及做完jeiba的結果(result)。 connectToDB中包含三個參數：
* mongoURL : 資料庫網址，要求型態為字串，此參數是必要的。
* dbName : 資料庫名稱，要求型態為字串，此參數是必要的。
* collectionName : 資料及名稱，要求型態為字串，此參數是必要的。

<br>

**使用範例:** 若想爬取2018年6月9日至2019年6月9日期間之文章，檔案存在本地端，31lab資料庫，dcard資料集，可輸入:
```
import dcard_scraper
connectToDB("xxx","xxx","xxx")
scrapDcard('makeup','20180609','20190609')
```


## 終端機下的使用方式

爬取2018年6月9日至2019年6月9日期間之文章，存在本地端，31lab資料庫，dcard資料集（預設）

    python dcard_scraper.py --forum makeup --start_date=2018-06-09 --end_date=2019-06-09

爬取2018年6月9日至2019年6月9日期間之文章，存在本地端，phoebe資料庫，dddcard資料集（更改db資訊）

    python dcard_scraper.py --forum makeup --start_date=2018-06-09  --dbURL= --end_date=2019-06-09 --dbName=phoebe --collectionName=dddard

其中可用的六個引數限制與使用如下:
* --forum : 預爬取資料之看板名稱，要求型態為字串,此參數是必要的。
* --start_date : 爬取之資料的起始日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，此參數是必要的。
* --end_date : 爬取之資料的結束日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，此參數是必要的。
* --dbURL : 資料庫網址，要求型態為字串，此參數是非必要的，預設是連接至本地端"mongodb://localhost:27017/"。
* --dbName : 資料庫名稱，要求型態為字串，此參數是非必要的，預設是"31lab"
* --collectionName : 資料及名稱，要求型態為字串，此參數是非必要的，預設是"dcard"

## 輸出db範例

    { 
        "_id" : NumberInt(231460541), 
        "forumAlias" : "makeup", 
        "artTitle" : "防曬", 
        "artDate" : "2019-06-09T16:11:58.490Z", 
        "artUrl" : "https://www.dcard.tw/_api/posts/231460541", 
        "cleanResult" : "各位大大有推薦的防曬用品嗎～主要防曬黑啊哈哈", 
        "result" : [
            {
                "sentences" : "各位大大有推薦的防曬用品嗎～主要防曬黑啊哈哈", 
                "tokens" : [
                    "各位", 
                    "大大", 
                    "有", 
                    "推薦", 
                    "的", 
                    "防曬", 
                    "用品", 
                    "嗎", 
                    "～", 
                    "主要", 
                    "防曬", 
                    "黑", 
                    "啊", 
                    "哈哈"
                ], 
                "POS" : [
                    "各位#SYM", 
                    "大大#SYM", 
                    "有#SYM", 
                    "推薦#SYM", 
                    "的#SYM", 
                    "防曬#SYM", 
                    "用品#SYM", 
                    "嗎#SYM", 
                    "～#SYM", 
                    "主要#SYM", 
                    "防曬#SYM", 
                    "黑#SYM", 
                    "啊#SYM", 
                    "哈哈#SYM"
                ]
            }
        ]
    }

## 使用上的限制以及可能遭遇的問題

dcard一次最多同時爬100則。

此程式使用多執行緒進行實作，但未提供從外部設定數量的操作，預設數量為90。若有更改需求請自行至dcard_scraper.py內進行更改。

## 需要預先安裝之套件

* dcard-spider
* pymongo
* requests
* bs4
* json
* StanfordCoreNLP
* jieba
* argparse


