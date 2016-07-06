import sys
import sqlite3
import markovgen
import twitter_init
import random
import char_class
from datetime import datetime, timedelta
import time

# database shit
conn = sqlite3.connect('seinfeld.db')
c = conn.cursor()
conn.text_factory = sqlite3.OptimizedUnicode

# twitter shit
twitter_api = twitter_init.init_account()

# speaker list
speakerList = []
speakerList.append(char_class.char_class('JERRY',      14645))
speakerList.append(char_class.char_class('GEORGE',      9613))
speakerList.append(char_class.char_class('ELAINE',      7967))
speakerList.append(char_class.char_class('KRAMER',      6656))
speakerList.append(char_class.char_class('NEWMAN',       625))
speakerList.append(char_class.char_class('MORTY',        502))
speakerList.append(char_class.char_class('HELEN',        470))
speakerList.append(char_class.char_class('FRANK',        429))
speakerList.append(char_class.char_class('SUSAN',        382))
speakerList.append(char_class.char_class('ESTELLE',      273))
speakerList.append(char_class.char_class('PETERMAN',     199))
speakerList.append(char_class.char_class('PUDDY',        163))
speakerList.append(char_class.char_class('LEO',          145))
speakerList.append(char_class.char_class('JACK',         124))
speakerList.append(char_class.char_class('STEINBRENNER', 122))
speakerList.append(char_class.char_class('MICKEY',       118))
speakerList.append(char_class.char_class('BANIA',        102))

def get_speaker_CDF():
	totalLines = sum(item.numLines for item in speakerList)
	for idx, item in enumerate(speakerList):
		item.probability = item.numLines/totalLines
		if idx != 0:
			item.cumulative = speakerList[idx-1].cumulative + item.probability
		else:
			item.cumulative = item.probability

get_speaker_CDF()

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

def get_char(speakers):
	randVal = random.random()
	for item in speakers:
		if randVal <= item.cumulative:
			return item.name
	return speakers[0].name

def generate_tweet_text():
	charName = get_char(speakerList)
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

def periodically_tweet():
	while True:
		tweet_out()
		numHours = random.randint(12,24)
		#print('now: ')
		#print(datetime.now())
		timeToTweet = datetime.now() + timedelta(hours=numHours)
		#print('tweet at: ')
		#print(timeToTweet)
		while datetime.now() < timeToTweet:
			time.sleep(60)
	
