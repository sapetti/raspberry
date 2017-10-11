#!/usr/bin/env python
import tweepy
import datetime
import os.path

# Twitter keys
CONSUMER_KEY = '[[CONSUMER_KEY]]'
CONSUMER_SECRET = '[[CONSUMER_SECRET]]'
ACCESS_KEY = '[[ACCESS_KEY]]'
ACCESS_SECRET = '[[ACCESS_SECRET]]'

def autenticate():
	# Authenticate
    	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    	return tweepy.API(auth)

def post_tweet(msg):
    	x = autenticate()
    	print 'Tweeting... ' + msg
    	x.update_status(msg)
    
def view_tweets():
    	x = autenticate()
    	print 'View tweets'
    	for tweet in x.user_timeline():
        	print(tweet.created_at)
        	print(tweet.text)
        	print('')

def post_media_tweet(msg, fname):
    	x = autenticate()
	print 'Tweeting media... ' + msg
	if(os.path.isfile(fname)):
		print 'File exists'
		fn = os.path.abspath(fname)
		print 'File path ' + fn
		x.update_with_media(fn, status=msg)
	else:
		print 'File does not exit'
	print 'Update end'
    

post_media_tweet('.', './PHOTO.JPG')
view_tweets()

