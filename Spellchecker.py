# -*- coding: utf-8 -*-
import time 
from difflib import SequenceMatcher
from datetime import datetime


print("\nWelcome to the spellchecker, hope you will have a good experience!!\n\n")
time.sleep(1)

#When print: box drawing for menu, │ for input, │ │ for invalid input, ┄ for feedback

#MENU
while True:

	#Valid input and menu
	while True:
		try:
			menuOp = int(input("╒======================================╕\n" 
							  +"│ Enter a number for:                  │\n" 
							  +"│ 1. Sentence spellcheck               │\n"
							  +"│ 2. File spellcheck                   │\n"
							  +"│ 0. Quit                              │\n"
							  +"╘======================================╛\n"
							  + "Your option:"))
			if (menuOp in (1, 2, 0)):
				break
		except ValueError:
			print("│ │ Please introduce a number!\n")

	#Sentence spellcheck
	if (menuOp == 1):
		text = input("\n│ May you please introduce your sentence:\n")

	#File spellcheck
	elif (menuOp == 2):
		while True:
			fileName = input("\n│ May you please introduce the filename: ")
			#Valid input
			try:
				file = open(fileName, "r")
				print("┄File opened!")
				text = file.read()
				file.close()
				fileBack = 0
				break
			except FileNotFoundError:
				print("│ │ Oops, it seems that not such file exist in your current directory, please check again!\n")
				#Valid input for going back
				try:
					fileBack = int(input("│ │ Enter 1 to introduce again file name, 2 to go back to menu:"))
					while fileBack not in (1, 2):
						print("│ │ Please enter 1 or 2!")
						fileBack = int(input("│ │ Enter 1 to introduce again file name, 2 to go back to menu:"))
					if (fileBack == 1):
						continue
					elif (fileBack == 2):
						break
				#The only imperfection is that once reached this option, it goes back to filename input directly. Can't use normal while, otherwise above's continue and break lose its function.
				except ValueError:
					print("│ │ Please introduce a number!\n")
		#To get back to menu
		if (fileBack == 2):
			fileBack = 0
			continue
	
	#Quit
	elif (menuOp == 0):
		time.sleep(1)
		print("\n\nThanks for using this spellchecker, have a nice day, bye!")
		break

	#Timer starts from now				
	start = time.time()

	#Filtering unwilling characters
	print("\n┄Eliminating unwilling characters....\n!!!Be aware that only english letters are allowed!!!")
	time.sleep(1)
	textFiltered = ""
	text = text.lower()
	for character in text:
		#For space and enter
		if (ord(character) not in (10, 32)):
			if (ord(character) < 97 or ord(character) > 122):
					character = ""
		textFiltered += character


	#Create word list
	toBeSpellchecked = textFiltered.split()

	#Load dictionary
	try:
		dictionaryFile = open("EnglishWords.txt", "r")
		dictionaryText = dictionaryFile.read()
		dictionaryFile.close()
		dictionary = dictionaryText.split()
	#In case EnglishWords is not available
	except FileNotFoundError:
		print("│ │ It seems that EnglishWords.txt isn't downloaded yet into current directory. Please make sure it is and try again.")

	#Initialising some variables
	correctCounter = 0
	incorrectCounter = 0
	totalWordCounter = 0
	dictionaryWordCounter = 0
	changedWordConter = 0
	spellcheckedText = ""

	#For loop to process all the words in the textFiltered
	for textWord in toBeSpellchecked:

		print("\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - \n\n"+
			"\n\n┄CHECKING FOR " + textWord +" IN THE DICTIONARY...")

		print(textWord + ":", end= " ")
		#List with each number corresponding to the similarity (with SequenceMatcher) to each words of dictionary
		similarity = []
		for dictionaryWord in dictionary:
			similarity.append(SequenceMatcher(None, textWord, dictionaryWord).ratio())
		
		#Index of the maximum value in similarity[]
		maxSimilarityIndex = similarity.index(max(similarity))	

		#Word is correct
		if (similarity[maxSimilarityIndex] == 1):
			print("is correct!\n")
			correctCounter += 1

		#Word not foundz
		else:
			print("not found in dictionary!\n")

			#Waiting for user to enter an option
			while True:
				try:
					wordOp = int(input("╒\n" 
									  +"│ Dealing with: "+ textWord +". Enter a number for:\n" 
									  +"│ 1. Allow the incorrect word\n"
									  +'│ 2. Mark the word with "¿?" at its beginning and end\n'
									  +"│ 3. Add this word to the dictionary as new word\n"
									  +"│ 4. Look for a suggestion word\n"
									  +"╘\n"
									  + "Your option:"))
					if (wordOp in (1, 2, 3, 4)):
						break
					else:
						print("│ │ Please introduce a valid number option!")
				except ValueError:
					print("│ │ Please introduce a number!\n")

			#Option 1
			if (wordOp == 1):
				print("┄Word allowed!\n")
				incorrectCounter += 1

			#Option 2
			elif (wordOp == 2):
				print('┄Word marked with "¿?" !\n')
				textWord = "¿" + textWord +"?"
				incorrectCounter += 1

			#Option 3
			elif (wordOp == 3):
				print("┄Adding this word to the dictionary!\n")
				dictionary.append(textWord)
				dictionaryWordCounter += 1
				correctCounter += 1

			#Option 4
			elif (wordOp == 4):
				print("┄Here is the suggestion word: " + dictionary[maxSimilarityIndex]
					+ "\n│ Enter 1 to change the original word by this suggestion, 0 to keep with the original word.")
				#Making sure of the user's input
				while True:
					suggestionOp = int(input("\nWhat do you want to do: "))
					try:
						if suggestionOp in (1, 0):
							break
						else:
							print("│ │ Please enter 1 or 0!")
					except ValueError:
						print("│ │ Please enter a number!")

				#If keep with the word
				if (suggestionOp == 0):
					print("┄Word kept!\n")
					incorrectCounter += 1

				#If changed the word
				if (suggestionOp == 1):
					print("┄Word changed to " + dictionary[maxSimilarityIndex] + "!\n")
					textWord = dictionary[maxSimilarityIndex]
					correctCounter += 1

		spellcheckedText = spellcheckedText + textWord + " " 

	totalWordCounter = incorrectCounter + correctCounter

	#Stop timer
	stop = time.time()
	timeLasted = ""
	seconds = int(stop - start)
	minutes = 0
	hours = 0
	#Transforming time
	while (seconds > 59):
		seconds -= 60
		minutes += 1
	while (minutes > 59):
		minutes -= 60
		hours += 1

	#Casting into string
	if (hours != 0 ):
		timeLasted = timeLasted + str(hours) + " hours, "
	if (minutes != 0 ):
		timeLasted = timeLasted + str(minutes) + " minutes and "
	timeLasted = timeLasted + str(seconds) + " seconds "

	#Current date and time
	now = datetime.now()
	nowString = now.strftime("%d/%m/%Y %H:%M:%S")

	#Summary statistics
	summaryStatistics = ("\n\n"+
	"STATISTICS OF THE SPELLCHECKING\n" +
	"-------------------------------\n"+
	" Total words spellchecked: " + str(totalWordCounter) + "\n"+
	" Number of words spelt incorrectly: " + str(incorrectCounter) + "\n"+
	" Number of words spelt correctly: " + str(correctCounter) + "\n"+
	" Number of words added to dictionary: " + str(dictionaryWordCounter) + "\n"+
	" Number of words words changed: " + str(changedWordConter) + "\n"+
	" Number of words added to dictionary: " + str(dictionaryWordCounter) + "\n"+
	" Time and date when spellchecked: " + nowString + "\n"+
	" Total time used in spellchecking: " + timeLasted + "\n")

	#This format is due to error on charmap occurs when try to write box drawing characters into the new file, therefore we print it only in the terminal and not in the new file
	print("\n\n▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"+
	      "\n\nWe are finishing text spellchecking. And now, a summary statistic will be displayed below.\n"+
	      "╭────────────────────────────────────────────────────────────────────────────────────────────────╮")
	print(summaryStatistics)
	print("╰────────────────────────────────────────────────────────────────────────────────────────────────╯")

	#Creating new file
	print("Creating new file for text after spellchecked...\n")
	time.sleep(2)
	newFileName = str(input("│ Please introduce a name for the new file. \nBe aware that the name must not be an existing file name, otherwise it will be replaced! (Remember to add file extension, i.e. '.txt' )\nNew file name: "))

	newFile = open(newFileName, "w")
	finalText = spellcheckedText + summaryStatistics
	newFile.write(finalText)
	newFile.close()
	time.sleep(2)
	print("\n┄File successfully created!\n")


	#End of spellchecker
	print("\n\nThis is the end of the spellchecker, glad that you have completed the spellchecking correctly! \n Now the program will return to the main menu, enter 0 if want to quit. Have a nice day!\n\n\n")
	print("===============================================================================\n\n\n")
	time.sleep(3)
	continue
				


