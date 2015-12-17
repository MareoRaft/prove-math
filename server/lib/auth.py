from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
from requests_oauthlib.compliance_fixes import linkedin_compliance_fix
import json
import xml.etree.ElementTree as ET

########################## Global Variables #############################
secret_array = []
with open('lib/auth_secrets.txt', 'r') as file:
	for line in file:
		secret = line.split('=')[1].rstrip()
		secret_array.append(secret)

fb_client_secret = secret_array[0]
google_client_secret = secret_array[1]
linkedin_client_secret = secret_array[2]
github_client_secret = secret_array[3]

############################## Methods ##################################
def auth_url_dict():
	url_dict = {}
	# for provider_name, provider in provider_dict.items():
	for provider_name in provider_dict.keys():
		url_dict[provider_name] = get_new_provider(provider_name).auth_url
	return url_dict

def facebook_id_and_pic(self,user_info,user_dict):
	r=json.loads(self.oauth_obj.get('https://graph.facebook.com/me?fields=first_name').text)
	user_dict['id_name']=r['first_name']
	user_dict['profile_pic']='https://graph.facebook.com/'+r['id']+'/picture'
	return user_dict

def linkedin_id_and_pic(self,user_info,user_dict):
	user_dict['id_name']=user_info.find('first-name').text
	pic_content=self.oauth_obj.get('https://api.linkedin.com/v1/people/~/picture-url')
	user_dict['profile_pic']= ET.fromstring(pic_content.text).text
	return user_dict

def google_id_and_pic(self,user_info,user_dict):
	user_dict['id_name']=user_info['given_name']
	url=self.oauth_obj.get('https://www.googleapis.com/plus/v1/people/'+user_info['id']+'?fields=image&key='+provider.oauth_obj.client_id)
	user_dict['profile_pic']=json.loads(url.text)['image']['url']
	return user_dict

def github_id_and_pic(self,user_info,user_dict):
	user_dict['id_name']=user_info['login']
	user_dict['profile_pic']=user_info['avatar_url']
	return user_dict

################################## Provider ###################################


class Provider:


	def __init__(self, name, client_id, redirect_uri, auth_url, token_url, request_url, secret, get_id_and_picture,
				 compliance_fix=(lambda x: x), scope=None, auth_url_params={}, request_format='json'):

		oauth2session = OAuth2Session(
			client_id=client_id,
			redirect_uri=redirect_uri,
			scope=scope
		)

		self.oauth_obj = compliance_fix(oauth2session)
		self.auth_url = auth_url
		self.name = name
		self.auth_url_params = auth_url_params
		self.token_url = token_url
		self.secret = secret
		self.request_url = request_url
		self.request_format = request_format
		self.get_id_and_picture=get_id_and_picture

		# self.is_token_fetched = False

	# def fetch_token(self): # not sure about this.  this would tie the provider to one persons account.  Then the provider could never be used for other people.
	# 	if self.is_token_fetched:
	# 		raise Exception('You should only fetch the token once.')
	# 	self.oauth_obj.fetch_token(
	# 		self.token_url,
	# 		client_secret=self.secret,
	# 		authorization_response=redirect_response
	# 	)
	# 	self.is_token_fetched = True

	@property
	def auth_url(self):
		if self.auth_url_params:
			return self.oauth_obj.authorization_url(self._auth_url, **self.auth_url_params)[0]
		else:
			return self.oauth_obj.authorization_url(self._auth_url)[0]

	@auth_url.setter
	def auth_url(self, new_url):
		self._auth_url = new_url


provider_dict = {
	'facebook': {
		'name': 'facebook',
		'client_id': '1614168325504559',
		'redirect_uri': 'http://localhost/index?method=fb',
		'auth_url': 'https://www.facebook.com/dialog/oauth',
		'token_url': 'https://graph.facebook.com/oauth/access_token',
		'request_url': 'https://graph.facebook.com/me?',
		'secret': fb_client_secret,
		'compliance_fix': facebook_compliance_fix,
		'get_id_and_picture': facebook_id_and_pic
	},
	'github': {
		'name': 'github',
		'client_id': '2b4b00568494cd73f15b',
		'redirect_uri': None,
		'auth_url': 'https://github.com/login/oauth/authorize',
		'token_url': 'https://github.com/login/oauth/access_token',
		'request_url': 'https://api.github.com/user',
		'secret': github_client_secret,
		'get_id_and_picture': github_id_and_pic
	},
	'linkedin': {
		'name': 'linkedin',
		'client_id': '771om0rwuhhpqh',
		'redirect_uri': 'http://localhost/index?method=linkedin',
		'auth_url': 'https://www.linkedin.com/uas/oauth2/authorization',
		'token_url': 'https://www.linkedin.com/uas/oauth2/accessToken',
		'request_url': 'https://api.linkedin.com/v1/people/~',
		'secret': linkedin_client_secret,
		'compliance_fix': linkedin_compliance_fix,
		'request_format': 'xml',
		'get_id_and_picture': linkedin_id_and_pic
	},
	'google': {
		'name': 'google',
		'client_id': '1008334791623-c2slo9fqrksbuac72krlnbq1tdlsgo64.apps.googleusercontent.com',
		'redirect_uri': 'http://localhost/index?method=google',
		'auth_url': "https://accounts.google.com/o/oauth2/auth",
		'token_url': "https://accounts.google.com/o/oauth2/token",
		'request_url': 'https://www.googleapis.com/oauth2/v1/userinfo',
		'secret': google_client_secret,
		'scope': [
			"https://www.googleapis.com/auth/userinfo.email",
			"https://www.googleapis.com/auth/userinfo.profile",
		],
		'auth_url_params': {
			'access_type': "offline",
			'approval_prompt': "force",
		},
		'get_id_and_picture':google_id_and_pic
	},
}

# def get_provider(name):
# 	if name == 'fb':
# 		name = 'facebook'
# 	return provider_dict[name]

def get_new_provider(name):
	if name == 'fb':
		name = 'facebook'
	return Provider(**provider_dict[name])
