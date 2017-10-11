from http_helper import CustomHTTPRedirectHandler
import http_helper

from poster import poster
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib
import urllib2

class FacebookClient(object):

	app_id='751693131538890'
	fb_login_url = 'https://www.facebook.com/login.php'
	fb_access_token_url = 'https://www.facebook.com/v2.1/dialog/oauth?response_type=token&client_id='+app_id+'&redirect_uri=https%3A%2F%2Fdevelopers.facebook.com%2Ftools%2Fexplorer%2Fcallback'
	fb_post_photo_url = 'https://graph.facebook.com/v2.1/645856582167140/photos'
	
	def __init__(self, email, password):
		super(FacebookClient, self).__init__()
		self.email = email
		self.password = password
		handlers = [CustomHTTPRedirectHandler, poster.streaminghttp.StreamingHTTPHandler(), poster.streaminghttp.StreamingHTTPSHandler()]

		self.opener = urllib2.build_opener(*handlers) 
		urllib2.install_opener(self.opener)	

		print 'Trying to login...'
		self.cookies = self.get_login_cookies(email, password)
		print 'Got cookies!'
		print 'Getting access_token...'
		self.access_token = self.get_access_token(self.cookies)
		print 'Got access_token: ' + self.access_token


	def get_login_cookies(self, email, password):	
		data = urllib.urlencode({'email': email, 'pass': password})

		self.opener.addheaders = [
			('cookie', 'reg_fb_gate=https%3A%2F%2Fwww.facebook.com'),
			('User-Agent', 'Chrome%2F36.0.1985.67+Safari%2F537.36')
		]

		try:
			response = self.opener.open(self.fb_login_url, data)
			if response.status == 302:
				cookies = http_helper.extract_cookies(response.redirect_headers)
				# check if login was successful
				if 'datr' in cookies:
					content = response.read()
					response.close()
					return cookies	
				
			raise Exception('Error doing request to Facebook! - (email/password?)')
		except urllib2.HTTPError as e:
			print e
			raise Exception('Error doing request to Facebook!')

	def get_access_token(self, cookies):
		
		self.opener.addheaders = [
			('User-Agent', 'Chrome%2F36.0.1985.67+Safari%2F537.36'),
			('Cookie', http_helper.get_cookies_kv(cookies))
		]

		try:
			response = self.opener.open(self.fb_access_token_url)
			location_header = http_helper.get_location_header(response.redirect_headers)
			if location_header == '':
				raise Exception('Error fetching access_token!')
			access_token_string = location_header.split('access_token=')[1]
			access_token = access_token_string.split('&expires_in=')[0]
			expires_in = access_token_string.split('&expires_in=')[1]
			print 'Token will expire in ' + expires_in + ' seconds'
			return access_token	
		except urllib2.HTTPError as e:
			print e
			raise Exception('Error fetching access_token!')	

	# uploads photo
	def upload_photo(self, photo_file):
		print "Posting photo..."
		datagen, headers = multipart_encode({'source': open(photo_file, 'rb'), 'access_token': self.access_token})
		request = urllib2.Request(self.fb_post_photo_url, datagen, headers)

		try: 
			response = urllib2.urlopen(request).read()
			print response
		except urllib2.HTTPError as e:
			print e.code
			print e.read() 
		return



		
