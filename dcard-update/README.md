
# Dcard_Update

更新Dcard 資料的爬蟲程式

## 使用方式
此程式用來更新MYSQL中Dcard資料至最新資料。

更新指定版面功能之函式為updateToLatest(forum)：於函式內依要求格式輸入指定的版，即可更新該文章至最新文章。
更新所有版面功能之函式為updateAllToLatest():執行則可更新所有版面（中山大學、女孩、追星、有趣、心情、時事、彩虹、感情、美妝）的文章。

updateToLatest包含一個參數(forum)：
* forum : 預爬取資料之看板名稱，要求型態為字串,此參數是必要的。若輸入 all，則可更新所有版面之文章。

例:若想更新中山版，可輸入:

    import update_dcard
    updateToLatest('nsysu')

例:若想更新所有版至最新文章，可輸入:

    import update_dcard
    updateAllToLatest()

## 終端機下的使用方式

更新中山版

    python update_dcard.py --forum nsysu 

更新所有版

    python update_dcard.py 

其中可用的一個引數限制與使用如下:
* --forum : 預爬取資料之看板名稱，要求型態為字串，此參數非必要的，預設 all，可爬所有版面。

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
