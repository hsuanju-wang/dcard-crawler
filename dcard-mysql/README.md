
# Dcard_Mysql

Dcard 網頁資料爬蟲程式，爬完後將資料存於Mysql。

## 使用方式

**爬蟲功能之函式為scrapDcard(post_alias,startDate,endDate)**：於函式內依要求格式輸入指定的版，指定的日期區間，即可爬取該日期區間內該版的所有文章。若startDate輸入-1，則從最早的文章開始爬，若endDate輸入-1，則爬至最新文章。

scrapDcard中包含三個參數(post_alias,startDate,endDate,collection)：
* post_alias : 預爬取資料之看板名稱，要求型態為字串,此參數是必要的。
* startDate : 爬取之資料的起始日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，輸入-1，則從最早的文章開始爬，此參數是必要的。
* endDate : 爬取之資料的結束日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，輸入-1，則爬至最新文章，此參數是必要的。

例:若想爬取中山版，2018年6月9日至2019年6月9日期間之文章，可輸入:

    import dcard_mysql
    scrapeDcard('nsysu','20180609','20190609')

例:若想爬取中山版，所有文章，可輸入:

    import dcard_mysql
    scrapeDcard('nsysu',-1,-1)

<br>

**不指定版面爬蟲功能之函式scrapDcardAll(startDate,endDate)：** startDate, endDate輸入方式如上述。取中山大學、女孩、追星、有趣、心情、時事、彩虹、感情、美妝，這9個比較熱門的版進行爬蟲。

scrapDcardAll包含2個參數(startDate,endDate)：
* startDate : 爬取之資料的起始日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，輸入-1，則從最早的文章開始爬，此參數是必要的。
* endDate : 爬取之資料的結束日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，輸入-1，則爬至最新文章，此參數是必要的。

例:若想爬取2018年6月9日至2019年6月9日期間之所有版面文章，可輸入:

    import dcard_mysql
    scrapDcardAll('20180609','20190609')

例:若想爬取所有版面之所有文章，可輸入:

    import dcard_mysql
    scrapeDcardAll(-1,-1)

<br>

**輸入至mysql：**
- database名稱是依照版面，如： "crawler_dcard_nsysu", "crawler_dcard_girl"
- table名稱是依照版面及年份，如："nsysu_2018","nsysu_2019"
- 若有已存在的database/table，則將爬到的資料直接新增進database/table
- 若尚未建立database/table，則會自動新增對應的database/table。



## 終端機下的使用方式

爬取2018年6月9日至2019年6月9日期間之中山版文章

    python dcard_mysql.py --forum nsysu --start_date=2018-06-09 --end_date=2019-06-09

爬取中山版所有文章

    python dcard_mysql.py --forum nsysu 

爬取所有版面之所有文章

    python dcard_mysql.py 

其中可用的三個引數限制與使用如下:
* --forum : 預爬取資料之看板名稱，要求型態為字串，此參數非必要的，預設 all，可爬所有版面。
* --start_date : 爬取之資料的起始日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，此參數非必要，預設-1，從最早的文章開始爬。
* --end_date : 爬取之資料的結束日期，要求型態為字串，輸入西洋年月日格式為YYYY-MM-DD，此參數非必要，預設-1，爬至最新文章，。


## 使用上的限制以及可能遭遇的問題

dcard一次最多同時爬100則。

此程式使用多執行緒進行實作，但未提供從外部設定數量的操作，預設數量為90。若有更改需求請自行至dcard_scraper.py內進行更改。

## 需要預先安裝之套件

* dcard-spider
* pymysql
* requests
* bs4
* json
* argparse
