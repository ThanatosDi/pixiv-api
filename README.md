# pixiv-api

Pixiv RESTful API

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/Kutinging/pixiv-api/tree/heroku)

# 使用
- ## GET /v1
   首頁
- ## GET /v1/illust/detail/{illust id}
   取得 作品(下稱:illsut) id 的詳細內容
- ## GET /v1/illust/list/{user id}
   取得 使用者(下稱:user)的 illsut 列表
- ## GET /v1/illust/search?keyword={keyword}&offset={offset}
   取得 關鍵字(下稱:keyword)的搜尋結果，offset 不輸入預設為 0 顯示0-29筆；offset=1 顯示 1-30筆，依此類推。
- ## GET /v1/rank/{timeinterval}?date={date}&offset={offset}
   取得 時間區間(下稱:timeinterval) **綜合** 排行榜，預設 offset 為 0 顯示0-29筆；offset=1 顯示 1-30筆，依此類推， date 為空。
   
  | timeinterval   |      意思      |date     |顯示排行         |
  |----------      |:-------------: |:------: |-------:        |
  | day            | 每日排行        |20181014 |2018-10-14排行|
  | week           | 每周排行        |20181014 |2018-10-08～2018-10-14排行|
  | month          | 每月排行        |20181014|2018-09-15～2018-10-14排行|
  
- ## GET /v1/rank/{timeinterval}/{mode}?date={date}&offset={offset}
   取得 timeinterval **個別** 排行榜，預設 offset 為 0 顯示0-29筆；offset=1 顯示 1-30筆，依此類推， date 為空。
  
  | timeinterval   |      意思      |mode|date     |顯示排行         |
  |----------      |:-------------: |:-:|:------: |-------:        |
  | day            | 每日排行        |male|20181014 |2018-10-14 受男性歡迎排行|
  |                |                |female|20181014|2018-10-14 受女性歡迎排行|
  |                |                |manga|20181014|2018-10-14 漫畫排行|
  | week           | 每周排行        |original|20181014 |2018-10-08～2018-10-14 原創排行|
  |                |                |rookie|20181014 |2018-10-08～2018-10-14 新人排行|
 - ## GET /v1/r18rank/{timeinterval}?date={date}&offset={offset}
   取得 timeinterval **綜合** R18排行榜，預設 offset 為 0 顯示0-29筆；offset=1 顯示 1-30筆，依此類推， date 為空。
   
   | timeinterval   |      意思      |date     |顯示排行         |
   |----------      |:-------------: |:------: |-------:        |
   | day            | 每日排行        |20181014 |2018-10-14 R18 排行|
   | week           | 每周排行        |20181014 |2018-10-08～2018-10-14 R18 排行|
  
- ## GET /v1/r18rank/{timeinterval}/{mode}?date={date}&offset={offset}
   取得 timeinterval **個別** R18排行榜，預設 offset 為 0 顯示0-29筆；offset=1 顯示 1-30筆，依此類推， date 為空。
  
  | timeinterval   |      意思      |mode|date     |顯示排行         |
  |----------      |:-------------: |:-:|:------: |-------:        |
  | day            | 每日排行        |male|20181014 |2018-10-14 R18 受男性歡迎排行|
  |                |                |female|20181014|2018-10-14 R18 受女性歡迎排行|
