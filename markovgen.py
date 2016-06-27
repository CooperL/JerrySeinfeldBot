import random

class Markov(object):
	
	def __init__(self, script_words):
		self.cache = {}
		self.words = script_words
		self.word_size = len(self.words)
		self.database()
	
	def triples(self):
		""" Generates triples from the given data string. So if our string were
				"What a lovely day", we'd generate (What, a, lovely) and then
				(a, lovely, day).
		"""
		
		if len(self.words) < 3:
			return
		
		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]

	def generate_markov_text(self):
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		while not seed_word[0].isupper():
			seed = random.randint(0, self.word_size-3)
			seed_word, next_word = self.words[seed], self.words[seed+1]
			# print(seed_word + '\n')
		w1, w2 = seed_word, next_word
		gen_words = []
		# while ((not rand_choice.endswith(('.','?','!'))) or (len(gen_words) < 5)):
		while True:
			gen_words.append(w1)
			rand_choice = random.choice(self.cache[(w1, w2)])
			w1, w2 = w2, rand_choice
			if w2.endswith(('.','?','!')) and len(gen_words) > 5:
				gen_words.append(w1)
				break
		gen_words.append(w2)
		return ' '.join(gen_words)




