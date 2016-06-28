import tweepy

def init_account():
	CONSUMER_KEY = 'Vpp5r1sm5Ai2zDZEdfvvtuAy2'#keep the quotes, replace this with your consumer key
	CONSUMER_SECRET = 'OVlyASOg6DyYpGSyxV2DFkrfP7XwUyYf9ySwCBrrDFip6YkKaZ'#keep the quotes, replace this with your consumer secret key
	ACCESS_KEY = '745765003052081152-ve196Gm6MuVHur5MuYbn6WAGB23zx2y'#keep the quotes, replace this with your access token
	ACCESS_SECRET = 'yfmughpu3mrG6AUtmIhBn95tuqK1O942BMnvAWzcMjGMP'#keep the quotes, replace this with your access token secret
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	return tweepy.API(auth)