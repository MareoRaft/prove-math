from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix

def get_secrets():
    secret_array=[]
    with open('oauth_secrets.txt','r') as file:
        for line in file:
            sec=line.split('=')[1].rstrip()
            secret_array.append(sec)
        
    return secret_array
        
def facebook_oauth():
    client_id ='1614168325504559'
    fb = OAuth2Session(client_id, redirect_uri='http://localhost/home?method=fb')
    fb = facebook_compliance_fix(fb)
    return fb

def google_oauth():
    client_id='1008334791623-c2slo9fqrksbuac72krlnbq1tdlsgo64.apps.googleusercontent.com'
    redirect_uri = 'http://localhost/home?method=google'
    scope=["https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile"]
    google = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
    return google

def linkedin_oauth():
    client_id='771om0rwuhhpqh'	
    linkedin = OAuth2Session(client_id, redirect_uri='http://localhost/home?method=linkedin')
    linkedin = linkedin_compliance_fix(linkedin)
    return linkedin

def github_oauth():
    client_id='2b4b00568494cd73f15b'
    github = OAuth2Session(client_id)
    return github

