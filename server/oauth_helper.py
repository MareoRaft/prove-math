################TO DOs###################################################
#put on localhost/form
#initialize method 
#global secret variable 


################Imports##################################################
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

################### Global Variables ####################################

sec_array=[]
with open('oauth_secrets.txt','r') as file:
    for line in file:
        sec=line.split('=')[1].rstrip()
        sec_array.append(sec)

fb_client_secret=sec_array[0]
google_client_secret=sec_array[1]
linkedin_client_secret=sec_array[2]
github_client_secret=sec_array[3]

###################### Methods###########################################


def dummy_func(g):
    return g

def get_authorization_urls(array_of_providers):
    urls={}
    for provider in array_of_providers:
        if provider.auth_url_params:
            address=provider.oauth_obj.authorization_url(provider.auth_url,**provider.auth_url_params)[0]
        else:
            address=provider.oauth_obj.authorization_url(provider.auth_url)[0]
        urls[provider.name]=address
    return urls

def get_facebook_oauth():
    fb=Provider(name='facebook',client_id ='1614168325504559',redirect_uri='http://localhost/home?method=fb',auth_url='https://www.facebook.com/dialog/oauth',token_url='https://graph.facebook.com/oauth/access_token',request_url='https://graph.facebook.com/me?',secret=fb_client_secret,compliance_fix=facebook_compliance_fix)
    return fb

def get_github_oauth():
    github=Provider(name='github',client_id='2b4b00568494cd73f15b',redirect_uri=None,auth_url='https://github.com/login/oauth/authorize',token_url='https://github.com/login/oauth/access_token',request_url='https://api.github.com/user',secret=github_client_secret)
    return github


def get_linkedin_oauth():
    linkedin=Provider(name='linkedin',client_id='771om0rwuhhpqh',redirect_uri='http://localhost/home?method=linkedin', auth_url='https://www.linkedin.com/uas/oauth2/authorization',token_url='https://www.linkedin.com/uas/oauth2/accessToken',request_url='https://api.linkedin.com/v1/people/~',secret=linkedin_client_secret,compliance_fix=linkedin_compliance_fix, request_format='xml')
    return linkedin

def get_google_oauth():
    google=Provider(name='google', client_id='1008334791623-c2slo9fqrksbuac72krlnbq1tdlsgo64.apps.googleusercontent.com',redirect_uri = 'http://localhost/home?method=google',auth_url="https://accounts.google.com/o/oauth2/auth",token_url="https://accounts.google.com/o/oauth2/token", request_url='https://www.googleapis.com/oauth2/v1/userinfo',secret=google_client_secret,scope=["https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile"],auth_url_params={'access_type':"offline", 'approval_prompt':"force"})
    return google


def initialize_login():
    fb=get_facebook_oauth()
    github=get_github_oauth()
    linkedin=get_linkedin_oauth()
    google=get_google_oauth()
    urls=get_authorization_urls([fb,linkedin,github,google])
    return urls

###########################Provider Class######################################
class Provider:
    def __init__(self,name,client_id,redirect_uri,auth_url,token_url,request_url,secret,compliance_fix=dummy_func,scope=None,auth_url_params={},request_format='json'):
        g=OAuth2Session(client_id=client_id,redirect_uri=redirect_uri,scope=scope)
        
        self.oauth_obj=[g,compliance_fix]
        self.auth_url=auth_url
        self.name=name
        self.auth_url_params=auth_url_params
        self.token_url=token_url
        self.secret=secret
        self.request_url=request_url
        self.request_format=request_format

    @property
    def request_format(self):
        return self._request_format

    @request_format.setter
    def request_format(self,new_request_format):
        self._request_format=new_request_format
    

    @property
    def request_url(self):
        return self._request_url

    @request_url.setter
    def request_url(self,new_request_url):
        self._request_url=new_request_url

    @property
    def token_url(self):
        return self._token_url
    
    @token_url.setter
    def token_url(self,new_token):
        self._token_url=new_token

    @property
    def secret(self):
        return self._secret

    @secret.setter
    def secret(self,new_secret):
        self._secret=new_secret


    @property
    def auth_url_params(self):
        return self._auth_url_params

    @auth_url_params.setter
    def auth_url_params(self, new_params):
        self._auth_url_params=new_params

    @property
    def oauth_obj(self):
        return self._oauth_obj

    @oauth_obj.setter
    def oauth_obj(self,list_required):
        self._oauth_obj=list_required[1](list_required[0])

    @property
    def auth_url(self):
        return self._auth_url
        
    @auth_url.setter
    def auth_url(self, new_url):
        self._auth_url=new_url

    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, new_name):
        self._name=new_name



    


    
    


