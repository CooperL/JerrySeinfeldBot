import sys
import sqlite3
import markovgen
import twitter_init

# database shit
conn = sqlite3.connect('seinfeld.db')
c = conn.cursor()
conn.text_factory = sqlite3.OptimizedUnicode

# twitter shit
twitter_api = twitter_init.init_account()

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

