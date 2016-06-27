import sys
import sqlite3
import markovgen
import tweepy

# database shit
conn = sqlite3.connect('seinfeld.db')
c = conn.cursor()
conn.text_factory = sqlite3.OptimizedUnicode

# twitter shit
CONSUMER_KEY = 'Vpp5r1sm5Ai2zDZEdfvvtuAy2'#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = 'OVlyASOg6DyYpGSyxV2DFkrfP7XwUyYf9ySwCBrrDFip6YkKaZ'#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = '745765003052081152-ve196Gm6MuVHur5MuYbn6WAGB23zx2y'#keep the quotes, replace this with your access token
ACCESS_SECRET = 'yfmughpu3mrG6AUtmIhBn95tuqK1O942BMnvAWzcMjGMP'#keep the quotes, replace this with your access token secret
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitter_api = tweepy.API(auth)

def get_lines(charName):
	# linesList = c.execute('SELECT sentence.text FROM sentence INNER JOIN \
	# 	utterance ON sentence.utterance_id=utterance.id WHERE \
	# 	utterance.speaker=? AND utterance.episode_id=?', \
	# 	(charName, epNum)).fetchall()
	linesList = c.execute('SELECT sentence.text FROM sentence INNER JOIN \
		utterance ON sentence.utterance_id=utterance.id WHERE \
		utterance.speaker=?', (charName,)).fetchall()
	return linesList

def tuples_to_words(tupleList):
	words = []
	for item in tupleList:
		currLine = item[0]
		lineWords = currLine.split()
		for word in lineWords:
			words.append(word)
	return words

def generate_tweet_text(charName):
	lines = get_lines(charName)
	words = tuples_to_words(lines)
	markov = markovgen.Markov(words)
	tweet = markov.generate_markov_text()
	while(len(tweet) > 140):
		tweet = markov.generate_markov_text()
	print(tweet)
	return tweet

def tweet_out(charName):
	tweet = generate_tweet_text(charName)
	twitter_api.update_status(tweet)

