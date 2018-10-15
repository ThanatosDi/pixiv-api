from flask import Flask,jsonify,request,make_response
import json
import requests
from pixivpy3 import *
from config import *
from exception import *

class mod:
    @staticmethod
    def add_two_dim_dict(dictionary,root,**value): 
        """新增修改二維字典\n
            dictionary  : 要新增修改的字典\n
            root        : 字典的字根(一維字典的鍵)\n
            value       : 傳入值 key=value 可複數，key為鍵 value為鍵值
        """
        dictionary[root] = {}
        for key in value.keys():
            dictionary[root][key] = value[key]
        return dictionary
    @staticmethod
    def datetransfer(date):
        return date[:4]+'-'+date[4:6]+'-'+date[6:]
    
class http:
    @staticmethod
    def status(message,status_code):
        return make_response(jsonify(message), status_code)

class PIXIV():
    """
    illustDetail(self,id)\n
    \t查詢 id 的作品詳細資料，id 為必須值\n
    illustList(userid,type='illust')\n
    \t查詢 userid 的作品列表詳細資料，userid 為必須值\n
    illustSearch(word,offset=None)\n
    \t搜尋 PIXIV 的作品中部分包含 word 的作品列表，word 為必須值\n\toffset 為可選
    """

    def __init__(self):
        self.api = AppPixivAPI()
        self.api.auth(config.Pixiv['username'],config.Pixiv['password'],'iw87X9CfgFhXDwV0Wgt5c0AhCgNqpaINJe5Fd5nbttk')
    
    def illustDetail(self,illustid):
        """
        取得 id 的作品詳細資料\n
        illustDetail(illustid)\n
        如該 id 的作品已刪除或不存在該作品 id 直接回傳空json，http status code = 200
        """
        try:
            illustdetail = self.api.illust_detail(illustid)
            if 'error' in illustdetail:
                raise illustDetailNotFound(f'illust {illustid} not found')
            return http.status(illustdetail.illust, 200)
        except illustDetailNotFound as e:
            return http.status({ },200)
        except Exception as e:
            return Interal_Server_Error(str(e))

    def illustList(self,userid,type='illust'):
        """
        取得 userid 的作品列表詳細資料\n
        illustList(userid)\n
        如該 userid 無作品或不存在該使用者直接回傳空json，http status code = 200
        """
        try:
            illustlist = self.api.user_illusts(userid,type='illust')
            if not any(illustlist['illusts']):
                raise illustListNotFound(f'user {userid} not found illust ilst')
            return http.status(illustlist, 200)
        except illustListNotFound as e:
            return http.status({ },200)
        except Exception as e:
            return Interal_Server_Error(str(e))
    
    def illustSearch(self,word,offset=None):
        """
        搜尋 word 的作品列表詳細資料\n
        illustSearch(word,offset=None)\n
        word 為必須搜尋關鍵字，offset 為可選預設0(None):顯示0~29筆 30:30~59筆依此類推\n
        """
        try:
            illust = self.api.search_illust(word,offset)
            return http.status(illust, 200)
        except Exception as e:
            return Interal_Server_Error(str(e))

    def illustRanking(self,mode=None, offset=None, date=None):
        try:
            if not date==None:
                date = (mod.datetransfer(date))
            ranking = self.api.illust_ranking(mode=mode,offset=offset,date=date)
            return http.status(ranking, 200)
        except Exception as e:
            return Interal_Server_Error(str(e))

    

class PIXIVR18:
    def __init__(self):
        self.apiR18 = AppPixivAPI()
        self.apiR18.auth(config.PixivR18['username'],config.PixivR18['password'],'_yAMBLPxLYQtVAK9BNn_6FSOPPnCzPjA-822ZA_OIlk')
    
    def illustR18Ranking(self,mode=None, offset=None, date=None):
        try:
            if not date==None:
                date = (mod.datetransfer(date))
            ranking = self.apiR18.illust_ranking(mode=f'{mode}_r18',offset=offset,date=date)
            return http.status(ranking, 200)
        except Exception as e:
            return Interal_Server_Error(str(e))

app = Flask(__name__)

class api:
    version = 'v1'

#GET / response 
@app.route(f"/{api.version}")
def home():
    return jsonify({'response':{'status':200,'message':'Welcome to Pixiv RESTful API website.','version':'1.0'}})

#GET /illust/detail data:{illust id:id,}
@app.route(f'/{api.version}/illust/detail/<int:id>')
def illust_detail(id):
    pixiv = PIXIV()
    return pixiv.illustDetail(id)

#GET /illust/list data:{user id:id,}
@app.route(f'/{api.version}/illust/list/<int:id>')
def illust_list(id):
    pixiv = PIXIV()
    return pixiv.illustList(id)

#GET /illust/search data:{keyword:word,}
@app.route(f'/{api.version}/illust/search')
def illust_search():
    word = request.args.get('keyword')
    offset = None
    if request.args.get('offset') :
        offset = request.args.get('offset')
    pixiv = PIXIV()
    return pixiv.illustSearch(word,offset)

# GET /rank/<string :timeinterval{'day', 'week', 'month'}>
# GET /rank/<string :timeinterval>/<string: mode{day:('male', 'female','manga'),week:('original','rookie'),month:()}>
@app.route(f'/{api.version}/rank/', defaults={'timeinterval': None})
@app.route(f'/{api.version}/rank/<string:timeinterval>')
@app.route(f'/{api.version}/rank/<string:timeinterval>', defaults={'mode': None})
@app.route(f'/{api.version}/rank/<string:timeinterval>/<string:mode>')
def illust_ranking(timeinterval,mode=None):
    pixiv = PIXIV()
    offset = None
    date = None
    if request.args.get('offset') :
        offset = request.args.get('offset')
    if request.args.get('date') :
        offset = request.args.get('date')
    timeintervallist = ('day', 'week', 'month')
    daymode = ('male', 'female','manga')
    weekmode = ('original','rookie')
    if timeinterval=='day' and mode in daymode:
       return pixiv.illustRanking(timeinterval+'_'+mode, offset, date)
    if timeinterval=='week' and mode in weekmode:
        return pixiv.illustRanking(timeinterval+'_'+mode, offset, date)
    if not timeinterval==None and mode==None and timeinterval in timeintervallist:
        return pixiv.illustRanking(timeinterval, offset, date) 
    return Page_Not_Found('404 not found')

# GET /rank/<string :timeinterval{'day', 'week'}>
# GET /rank/<string :timeinterval/<string :mode{day:('male', 'female'),week:()}>
@app.route(f'/{api.version}/r18rank/', defaults={'timeinterval': None})
@app.route(f'/{api.version}/r18rank/<string:timeinterval>')
@app.route(f'/{api.version}/r18rank/<string:timeinterval>', defaults={'mode': None})
@app.route(f'/{api.version}/r18rank/<string:timeinterval>/<string:mode>')
def illust_r18ranking(timeinterval,mode=None):
    pixiv = PIXIVR18()
    offset = None
    date = None
    if request.args.get('offset') :
        offset = request.args.get('offset')
    if request.args.get('date') :
        offset = request.args.get('date')
    timeintervallist = ('day', 'week')
    daymode = ('male', 'female')
    if timeinterval=='day' and mode in daymode:
       return pixiv.illustR18Ranking(timeinterval+'_'+mode, offset, date)
    if not timeinterval==None and mode==None and timeinterval in timeintervallist:
        return pixiv.illustR18Ranking(timeinterval, offset, date) 
    return Page_Not_Found('404 not found')

@app.errorhandler(404)
def Page_Not_Found(e):
    return http.status({'status_codde':404,'message':str(e)} , 404)

@app.errorhandler(500)
def Interal_Server_Error(e):
    if e is None:
        return http.status({'status_codde':500,'message':'500 Interal Server Error'} , 500)
    return http.status({'status_codde':500,'message':str(e)} , 500)



if __name__ == "__main__":
    app.run()