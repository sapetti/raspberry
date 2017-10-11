	
import urllib2

class CustomHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_302(self, req, fp, code, msg, headers):
		response = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
		response.status = code
		response.redirect_headers = headers.headers
		return response

	http_error_301 = http_error_302

def extract_cookies(headers):
	cookies_dict = {}
	for header in headers:
		if header.startswith('Set-Cookie: '):
			cookie_value = header.split('Set-Cookie: ')[1][:-2]
			cookies_dict[cookie_value.split('=')[0]]=cookie_value
	return cookies_dict

def get_cookies_kv(cookies):
	cookies_kv = ''
	for cookie in cookies:
		cookies_kv = cookies_kv + cookies[cookie].split('; ')[0] + '; '
	return cookies_kv

def get_location_header(headers):
	for header in headers:
		if header.startswith('Location: '):
			return header.split('Location: ')[1][:-2]
	return ''