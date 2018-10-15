import os
class config:
    Domain = '127.0.0.1:5000'
    Pixiv = {'username':os.environ['Pixiv_username'],'password':os.environ['Pixiv_password'],'refresh_token':os.environ['Pixiv_refresh_token']}
