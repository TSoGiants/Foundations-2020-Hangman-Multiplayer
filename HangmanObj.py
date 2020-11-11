from numpy import random
import string

def main():
	game = Hangman()

	while not game.game_won and not game.game_lost:
		print(game)
		while True: # Input loop.
			result = game.makeGuess(input("What is your guess? "))
			print(result[1]) # Print whatever string Hangman.makeGuess() returns.
			if result[0]:
				break
		
	print(game)

class Hangman:
	def __init__(self, min_letters=4, max_letters=8):
		if min_letters > max_letters:
			min_letters = max_letters

		words = []
		with open("word_list.txt", "r") as f:
			word_list = f.read()
			word_list = word_list.split()
			for word in word_list:
				if len(word) >= min_letters and len(word) <= max_letters:
					words.append(word)
		n = random.randint(len(words))
		self.word = words[n]
		self.progress = []
		for c in self.word:
			self.progress.append("_")
		
		self.guesses = []
		self.wrong_guesses = 0
		self.game_lost = False
		self.game_won = False
		
	def __str__(self):
		"""
		  +---+
		  |   |
		  O   |
		 /|\  |
		 / \  |
			  |
		=========
		"""		

		### Generate first line:
		s = "  +---+"
		s += "\n"
		
		### Generate second line:
		s += "  |   |"
		s += "\n"
		
		### Begin third line:
		if self.wrong_guesses > 0:
			s += "  O   |"
		else:
			s += "      |"
		s += "\n"
			
		### Begin fourth line:
		s += " "
		if self.wrong_guesses > 3:
			s += "/|\x5C"	# Left arm, torso, and right arm.
							# Note: Have to use hexadecimal code for backslash 
							# because backslash is an escape character.
		elif self.wrong_guesses > 2:
			s += "/| "	# Left arm and torso.
		elif self.wrong_guesses > 1:
			s += " | "	# Torso only.
		else:
			s += "   "  # Space for arms and torso but none displayed.
		s += "  |"	# Rest of gallows.
		s += "\n"
		
		### Begin fifth line:
		s += " "
		if self.wrong_guesses > 5:
			s += "/ \x5C"	# Left and right leg.
							# Note: Have to use hexadecimal code for backslash 
							# because backslash is an escape character.
		elif self.wrong_guesses > 4:
			s += "/  "	# Left leg only.
		else:
			s += "   "	# Space for legs but none displayed.
		s += "  |"	# Rest of gallows.
		s += "\n"
		
		### Begin sixth line:
		s += "      |"
		s += "\n"
		
		### Begin seventh line:
		s += "========="
		s += "\n"
		
		### Begin progress line:
		s += "\n"
		s += self.parseProgress()
		s += "\n"
		
		"""
		### Begin game state line:
		if self.game_won:
			s += "\n"
			s += "YOU WIN!!!"
		elif self.game_lost:
			s += "You lose. The word was '" + self.word + "'."
		"""
		return s
		
	def parseProgress(self):
		output = ""
		for letter in self.progress:
			output += letter.upper() + " "
		return output
		
	def makeGuess(self, guess):
		if not self.game_lost and not self.game_won:
			guess = str(guess).lower()
			
			if len(guess) == 1 and guess in string.ascii_lowercase:
				if guess not in self.guesses:
					self.guesses.append(guess)
					if guess in self.word:
						indices = []
						for i in range(len(self.word)):
							if guess == self.word[i]:
								indices.append(i)
						if len(indices) > 1:
							s = "s."
						else:
							s = "."
						s = "The word contains " + str(len(indices)) + " '" + guess.upper() + "'" + s
						for i in indices:
							self.progress[i] = guess.upper()
							
						self.updateGamestate()
					else:
						s = "Not a match."
						self.wrong_guesses += 1
						self.updateGamestate()
				else:
					s = "You've already guessed that letter. Please try again."
			else:
				s = "That guess is not formatted correctly. Please try again."
			
			if self.game_won:
				s = "YOU WIN!!!"
			elif self.game_lost:
				s = "You lose. The word was '" + self.word + "'."
		else:
			if self.game_won:
				s = "You already won this round. Please start a new game."
			else:
				s = "This game is already complete. Please start another."	
		
			
		return s
			
			
	def updateGamestate(self):
		if "_" not in self.progress:
			self.game_won = True
		elif self.wrong_guesses > 5:
			self.game_lost = True
			
if __name__ == "__main__":
	main()