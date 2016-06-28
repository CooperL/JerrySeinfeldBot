import sys
import sqlite3
import markovgen
import twitter_init
import random

# database shit
conn = sqlite3.connect('seinfeld.db')
c = conn.cursor()
conn.text_factory = sqlite3.OptimizedUnicode

# twitter shit
twitter_api = twitter_init.init_account()

# speaker list
speaker_list = ['JERRY', 'GEORGE', 'ELAINE', 'KRAMER', 'NEWMAN', 'MORTY', \
	'HELEN', 'FRANK', 'SUSAN', 'ESTELLE', 'PETERMAN', 'PUDDY', 'LEO', \
	'JACK', 'STEINBRENNER', 'MICKEY']

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

def get_char():
	idx = random.randint(0, (len(speaker_list)-1))
	return speaker_list[idx]

def generate_tweet_text():
	charName = get_char()
	lines = get_lines(charName)
	words = tuples_to_words(lines)
	markov = markovgen.Markov(words)
	tweet = charName + ': ' + markov.generate_markov_text()
	while(len(tweet) > 140):
		tweet = charName + ': ' + markov.generate_markov_text()
	print(tweet)
	return tweet

def tweet_out():
	tweet = generate_tweet_text()
	twitter_api.update_status(tweet)

