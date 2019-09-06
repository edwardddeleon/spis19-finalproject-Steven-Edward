"""
Authors: Edward De Leon and Steven Nguyen
Mentor: Amrit Singh
SPIS 2019 Final Project
"""


import markovify
import random
import twint
import csv
import os


# # # # # # # # # # # # #
# Variables/containers  #
# # # # # # # # # # # # #


# Dividing line used for organization
divider = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"


# Dictionary which holds models
models = {
	"BarackObama": [],
	"HillaryClinton": [], 
	"AOC": [], 
	"SenSanders": [], 
	"realDonaldTrump": [], 
	"MittRomney": [], 
	"senatemajldr": [], 
	"benshapiro": []
}


# Dictionary which holds weights
weights = {
	"BarackObama": 1,
	"HillaryClinton": 1, 
	"AOC": 1, 
	"SenSanders": 1, 
	"realDonaldTrump": 1, 
	"MittRomney": 1, 
	"senatemajldr": 1, 
	"benshapiro": 1
}


# Dictionary which holds political affiliation of default users
affiliation = {
	"BarackObama": "D",
	"HillaryClinton": "D", 
	"AOC": "D", 
	"SenSanders": "D", 
	"realDonaldTrump": "R", 
	"MittRomney": "R", 
	"senatemajldr": "R", 
	"benshapiro": "R"
}


# # # # # # # 
# Functions #
# # # # # # #


def scrape(user):
	""" Scrapes Tweets from given Twitter account """
	
	c = twint.Config()
	
	# Configuration/customization
	c.Username = user # Specifies account 
	c.Limit = 100 # Amount of Tweets to be scraped
	c.Filter_retweets = True # Filters retweets so there is only spelling/vocabulary from original user
	c.Store_csv = True # Stores as .csv file
	c.Links = "exclude" # Excludes urls/links
	
	# Sets name of file and scrapes
	cwd = os.getcwd() # Gets current working directory
	filepath = os.path.join(cwd, "data", user + ".csv") # Sets the filepath
	c.Output = filepath # Sets file name
	twint.run.Search(c) # Begins scraping


def clean(user):
	""" Moves Tweets to new .csv file """
	
	input  = str(user) + ".csv"
	output = str(user) + "_cleaned.csv"
	cwd = os.getcwd() # Gets current working directory
	
	if os.path.exists(os.path.join(cwd, "data", input)) == True: # Checks if input file is in data folder
		with open(os.path.join(cwd, "data", output), "w", newline = "", encoding = "utf-8") as output: # Creates output .csv file
			filewriter = csv.writer(output) # filewriter writes sequences
			with open(os.path.join(cwd, "data", input), "r", encoding = "utf-8") as input: # Opens input .csv file
				pointreader = csv.reader(input, quoting = csv.QUOTE_NONE) # pointreader reads sequences
				next(pointreader) # Skips header row
				for row in pointreader:
					filewriter.writerow([row[10].strip('"')]) # Moves Tweets from input to output

	
def scrape_clean():	
	""" Combines scrape and clean functions for every element in a list """
	for user in usernames:
		scrape(user) # Scrapes Tweets from every user in a list	
		try:
			clean(user) 
		except IndexError:
			pass


def train(user):
	""" Creates a model for singular user """
	model_list = [] # List where the model for each row (each Tweet) will be stored
	input_file = str(user) + "_cleaned.csv" # Sets filename which should be opened
	cwd = os.getcwd() # Gets current working directory
	with open(os.path.join(cwd, "data", input_file), "r", encoding = "utf-8-sig") as input: # Opens input .csv file
		pointreader = csv.reader(input) # pointreader reads sequences
		for row in pointreader:
			model_list.append(markovify.Text(row[0], well_formed = False)) # Adds model for each Tweet to model_list
		user_model = markovify.combine(model_list) # Combines model for each Tweet into one model
		return user_model
		
			
def trainAll():
	""" Trains every user in the models dictionary """
	for model in models:
		models[model] = train(model)

		
def generate(account):
	""" Generates a Tweet combining every model in the 'models' dictionary """
	model_list = [] # List where the model for each person will be stored
	weight_list = [] # List where the weight for each person will be stored
	if account in weights:
		weights[account] += 4 # Increases weight of specified user the most
	if account in affiliation: # Checks if the specified user has an affiliated party
		party = affiliation.get(account) # Gets user's affiliated party
		for user in affiliation:
			if affiliation.get(user) == party: # Checks for users in the same party
				if user != account:
					weights[user] += 2 # Increases weight of all other users in the same party slightly
	for weight in weights:
		weight_list.append(weights[weight]) # Adds each weight to weight_list to be combined
	for model in models:
		model_list.append(models[model]) # Adds each model to model_list to be combined
	combinedModel = markovify.combine(model_list, weight_list) # Combines each model in model_list together
	print("GENERATED TWEET:")
	print(combinedModel.make_short_sentence(280)) # Generates the Tweet


def generateUser(account):
	""" Generates a Tweet based on a single user's model """
	if account in weights:
		weights[account] += 4 # Increases weight of specified user the most
	if account in affiliation: # Checks if the specified user has an affiliated party
		party = affiliation.get(account) # Gets the user's affiliated party
		for user in affiliation:
			if affiliation.get(user) == party: # Checks for users in the same party
				if user != account:
					weights[user] += 2 # Increases weight of all other users in the same party slightly
	print("GENERATED TWEET:")
	print(models[account].make_short_sentence(280)) # Generates the Tweet


def generateParty(party_choice):
	""" Generates a Tweet based on the combined models of a particular political affiliation """
	model_list = [] # List where the model for each person will be stored
	weight_list = [] # List where the weight for each person will be stored
	for user in affiliation:
		if affiliation.get(user) == party_choice: # Checks if user's affiliation is the same as the given party
			weights[user] += 2 # Increases weight of all users in the same party slightly
			weight_list.append(weights[user]) # Adds user's weight to weight_list to be combined
			model_list.append(models[user]) # Adds user's model to model_list to be combined
	combinedModel = markovify.combine(model_list, weight_list) # Combines each model in model_list together
	print("GENERATED TWEET:")
	print(combinedModel.make_short_sentence(280)) # Generates the Tweet

	
def printwSpacing(string):
	""" Used for spacing/organization in command prompt/terminal """
	print(divider)
	print()
	print(str(string))
	print()

	
def addNewUser(user):
	""" Adds a new user to the 'models' dictionary """
	cwd = os.getcwd()
	input = str(user) + ".csv"
	if user not in models: # Checks if user is already in the models dictionary
		try: 
			print(divider)
			if os.path.exists(os.path.join(cwd, "data", input)) == False:
				scrape(user) # Scrapes Tweets of user
			clean(user) # Moves Tweets to a cleaner file
			models.update({str(user): []}) # Adds user to models
			weights.update({str(user): 1}) # Adds user to weights
			models[user] = train(user) # Creates a model for user and adds it as the user's value
			print(divider)
		except:
			print(divider)
			print("Please choose a Twitter account which exists.")
			models.pop(user) # Removes user from models if error occurs
			weights.pop(user) # Removes user from weights if error occurs
			print(divider)
			pass
	
	
def parseInput():
	""" Text user interface """
	print(divider)
	print()
	print('Would you like to choose from our list, add your own user, or check the current weights? \n Type "1" for our list or "0" for custom. \n Type "weight" to see the current weights.') # Prints out options
	print()
	response = input().strip()  # Removes all white space before and after sentence
	print()
	while response != "1" and response != "0" and response != "weight": # Repeat previous step if input is invalid
		printwSpacing('Would you like to choose from our list or add your own user? \n Type "1" for our list or "0" for custom. \n Type "weight" to see the current weights.')
		print()
		response = input().strip()  # Removes all white space before and after sentence
		print()
	if response == "1": # If user wants to use current list
		print()
		print("Here is the current list:")
		print()
		for model in models:
			print(model) # Prints out list of every model in models
		print()
		printwSpacing("Would you like the text to sound like a combination (2), a specific party (1), or only this user (0)?") # Prints out options
		print()
		response = input().strip()  # Removes all white space before and after sentence
		while response != "2" and response != "1" and response != "0": # Repeat previous step if input is invalid
			printwSpacing("Would you like the text to sound like a combination (2), a specific party (1), or only this user (0)?")
			response = input().strip()  # Removes all white space before and after sentence
		if response == "2": # If user wants a combination
			print()
			printwSpacing("Please input a user on the list.") # Prints out instructions
			print()
			response = input().strip()  # Removes all white space before and after sentence
			print()
			while response not in models: # Repeat previous step if input is invalid
				printwSpacing("Please input a user on the list.")
				print()
				response = input().strip()  # Removes all white space before and after sentence
				print()
			generate(response) # Generates Tweet which is a combination of all users in the models dictionary
			print()
		if response == "1": # If user wants a specific party
			print()
			printwSpacing("Please choose Republican (R) or Democrat (D).") # Prints out instructions
			print()
			response = input().strip()  # Removes all white space before and after sentence
			print()
			while response != "R" and response != "D": # Repeat previous step if input is invalid
				printwSpacing("Please choose Republican (R) or Democrat (D).")
				print()
				response = input().strip()  # Removes all white space before and after sentence
				print()
			generateParty(response) # Generates Tweet which is a combination of all users in specified party
			print()
		if response == "0": # If user wants a Tweet based on a single account
			print()
			printwSpacing("Please input a user on the list.") # Prints instructions
			print()
			response = input().strip()  # Removes all white space before and after sentence
			print()
			while response not in models: # Repeat previous step if input is invalid
				printwSpacing("Please input a user on the list.")
				print()
				response = input().strip()  # Removes all white space before and after sentence
				print()
			generateUser(response) # Generates Tweet based on single account
			

	if response == "0": # If user wants to input their own account
		printwSpacing("Please enter a valid Twitter username.")
		print()
		user = input().strip() # Removes all white space before and after sentence
		print()
		try:
			addNewUser(user) # Adds user to the dictionaries models and weights
		except:
			print("There was an error! Please try a different user.")
			pass
		trainAll() # Trains all users in the models dictionary
		while user not in models: # Repeat previous step if input is invalid
			print()
			printwSpacing("Please enter a valid Twitter username.")
			print()
			user = input().strip() # Removes all white space before and after sentence
			try:
				addNewUser(user)
			except:
				print("There was an error! Please try a different user.")
				pass
			print()
		print()
		print("Would you like the text to sound like a combination (1) or only this user (0)?") # Prints out options
		print()
		response = input().strip()  # Removes all white space before and after sentence
		print()
		while response != "1" and response != "0": # Repeat previous step if input is invalid
			printwSpacing("Would you like the text to sound like a combination (1) or only this user (0)?")
			print()
			response = input().strip()  # Removes all white space before and after sentence
			print()
		if response == "1": # If user wants a combination
			generate(user) # Generates Tweet which is a combination of all users in the models dictionary
		if response == "0": # If user wants a Tweet based on a single account
			generateUser(user) # Generates Tweet based on a single account
	
	if response == "weight": # If user wants to check the weights
		print()
		print(weights)
		print()

while True: # Infinite loop which re-runs the functions after parseInput() finishes
	trainAll() # Trains all models; otherwise, the Tweets cannot be generated
	parseInput() # Allows user to place inputs
