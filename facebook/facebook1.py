import urllib2, cookielib, re, os, sys

FACEBOOK_APP_ID = '[[APP_ID]]'
FACEBOOK_APP_SECRET = '[[APP_SECRET]]'


class Facebook():
    def __init__(self, email, password):
        self.email = email
        self.password = password

        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        opener.addheaders = [('Referer', 'http://login.facebook.com/login.php'),
                            ('Content-Type', 'application/x-www-form-urlencoded'),
                            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]
        self.opener = opener

    def login(self):
        url = 'https://login.facebook.com/login.php?login_attempt=1'
        data = "locale=sp_ES&non_com_login=&email="+self.email+"&pass="+self.password+"&lsd=20TOl"

        usock = self.opener.open('http://www.facebook.com')
        usock = self.opener.open(url, data)
	print usock.read()
	if "access" in usock.read():
		print usock.read()
		print "access in usock"
        if "Logout" in usock.read():
            print "Logged in."
        else:
            print "failed login"
            print usock.read()
            sys.exit()

    def getAuth(self):
        args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=self.request.path_url)
	"""redirect_url points to */login* URL of our app"""
	args["client_secret"] = FACEBOOK_APP_SECRET  #facebook APP Secret
	args["code"] = self.request.get("code")
	response = cgi.parse_qs(urllib.urlopen(
	    "https://graph.facebook.com/oauth/access_token?" +
	    urllib.urlencode(args)).read())
	access_token = response["access_token"][-1]
	return access_token

f = Facebook("[[EMAIL]]", "[[PASSWORD]]")
f.login()
print f.getAuth()
