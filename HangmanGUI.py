from tkinter import *
from HangmanObj	import Hangman
import string

class App:

	def __init__(self, master):
	
		self.game = Hangman()
		
		master.title("Hangman GUI")
		master.iconbitmap('favicon.ico')
		
		master.geometry("600x800")
		master.resizable(False, False)
		master.configure(background='#000000')
		
		self.display = Label(
			master, text=str(self.game), font=("Courier New", 32),
			fg = '#FFFFFF',
			bg = '#000000'
			)
		self.display.pack()

		self.letters = Text(
			master, font=("Courier New", 28), height = 1,
			foreground = '#AAAAAA',
			background = '#FFFFFF',
			selectbackground='#FFFFFF',
			selectforeground='#AAAAAA',
			insertontime=0
			)
			
		self.letters.tag_configure('tag-center', justify='center')
		self.letters.tag_configure('tag-good', foreground='#00FF00')
		self.letters.tag_configure('tag-bad', foreground='#FF0000')
		
		self.letters.insert(INSERT, string.ascii_uppercase, 'tag-center')
		self.letters.config(state=DISABLED)
		
		
		self.letters.pack()
		
		self.spacer = Frame(master, height=40, bg='#000000')
		self.spacer.pack()
		
		self.message = Label(
			master, text="To make a guess, please press a key on the keyboard.", font=("Arial Narrow", 32),
			fg = '#FFFFFF',
			bg = '#000000',
			wraplength=600
			)
		self.message.pack()
		
		self.reset = Button(
			master, text="New Game", command=self.restart,
			fg='#AAAAAA',
			bg='#333333',
			width=600,
			font=("Arial Narrow", 28),
			borderwidth=0
			)
		self.reset.pack(side=BOTTOM)
		
		master.bind('<Key>', self.key)
		
	def key(self, event):
		guess = str(event.char)
		#print("pressed: " + str(event.char))
		s = self.game.makeGuess(guess)
		self.message['text'] = s
		self.display['text'] = str(self.game)
		for i in range(len(string.ascii_lowercase)):
			if string.ascii_lowercase[i] in self.game.guesses:
				if string.ascii_lowercase[i] in self.game.word:
					# Good guess.
					self.letters.tag_add('tag-good', '1.' + str(i), '1.' + str(i+1))
				else:
					# Bad guess.
					self.letters.tag_add('tag-bad', '1.' + str(i), '1.' + str(i+1))
				
	def restart(self):
		self.game = Hangman() # Initialize new game.
		self.message['text'] = "To make a guess, please press a key on the keyboard."
		self.display['text'] = str(self.game)
		self.letters.tag_remove('tag-good', '1.0', 'end')
		self.letters.tag_remove('tag-bad', '1.0', 'end')

root = Tk()

app = App(root)

root.mainloop()