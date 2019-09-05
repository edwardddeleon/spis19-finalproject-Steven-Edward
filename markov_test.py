import markovify
import random
import twint
import csv
import os

def scrape(user):
	""" Scrapes Tweets from given Twitter account """
	
	c = twint.Config()
	
	# Configuration/customization
	c.Username = user
	c.Limit = 20
	c.Filter_retweets = True
	c.Store_csv = True
	c.Links = "exclude"
	
	# Sets name of file and scrapes
	cwd = os.getcwd()
	filename = os.path.join(cwd, "data", user + ".csv")
	c.Output = filename
	twint.run.Search(c)


def clean(user):
	""" Moves Tweets to new .csv file """
	
	input  = str(user) + ".csv"
	output = str(user) + "_cleaned.csv"
	cwd = os.getcwd() # gets current working directory
	
	# Creates output .csv file
	if os.path.exists(os.path.join(cwd, "data", input)) == True:
		with open(os.path.join(cwd, "data", output), "w", newline = "", encoding = "utf-8") as output:
			filewriter = csv.writer(output)
			# Opens input .csv file, skips header 
			with open(os.path.join(cwd, "data", input), "r", encoding = "utf-8") as input:
				pointreader = csv.reader(input, quoting = csv.QUOTE_NONE)
				next(pointreader)
				# Moves Tweets from input to output
				for row in pointreader:
					filewriter.writerow([row[10].strip('"')])

	
def scrape_clean():	
	""" Combines scrape and clean functions """
	for user in usernames:
		scrape(user)	
		try:
			clean(user)
		except IndexError:
			pass

divider = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"

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


def train(user):
	model_list = []
	input_file = str(user) + "_cleaned.csv" # sets filename which should be opened
	cwd = os.getcwd() # gets current working directory
	with open(os.path.join(cwd, "data", input_file), "r", encoding = "utf-8-sig") as input: # 
		pointreader = csv.reader(input)
		for row in pointreader:
			model_list.append(markovify.Text(row[0], well_formed = False))
		user_model = markovify.combine(model_list)
		return user_model
		
			
def trainAll():
	for model in models:
		models[model] = train(model)
		
def generate(account):
	model_list = []
	weight_list = []
	if account in weights:
		weights[account] *= 3
	if account in affiliation:
		party = affiliation.get(account)
		for user in affiliation:
			if affiliation.get(user) == party:
				if user != account:
					weights[user] *= 1.5
	for weight in weights:
		weight_list.append(weights[weight])
	for model in models:
		model_list.append(models[model])
	test = markovify.combine(model_list, weight_list)
	print(test.make_short_sentence(280))


def generateUser(account):
	if account in weights:
		weights[account] *= 3
	if account in affiliation:
		party = affiliation.get(account)
		for user in affiliation:
			if affiliation.get(user) == party:
				if user != account:
					weights[user] *= 1.5
	print(models[account].make_short_sentence(280))


def generateParty(party_choice):
	model_list = []
	weight_list = []
	for user in affiliation:
		if affiliation.get(user) == party_choice:
			weights[user] *= 1.5
			weight_list.append(weights[user])
			model_list.append(models[user])
	test = markovify.combine(model_list, weight_list)
	print(test.make_short_sentence(280))
	
def printwSpacing(string):
	print(divider)
	print()
	print(str(string))
	print()

	
def addNewUser(user):
	if user not in models:
		try:
			print(divider)
			scrape(user)
			clean(user)
			models.update({str(user): []})
			weights.update({str(user): 1})
			models[user] = train(user)
			print(divider)
		except:
			print(divider)
			print("Please choose a Twitter account which exists.")
			models.pop(user)
			weights.pop(user)
			print(divider)
			pass
	
	
def parseInput():
	print(weights) # remove this later
	printwSpacing("Would you like to choose from our list or add your own user? \n Type '1' for our list or '0' for custom")
	print(divider)
	print()
	response = input().strip()
	print()
	while (response != "1") and (response != "0"):
		printwSpacing("Would you like to choose from our list or add your own user? \n Type '1' for our list or '0' for custom")
		print(divider)
		print()
		response = input().strip()
		print()
	if response == "1":
		print()
		print(divider)
		print()
		print("Here is the current list:")
		print()
		for model in models:
			print(model)
		print()
		printwSpacing("Would you like the text to sound like a combination (2), a specific party (1), or only this user (0)?")
		print()
		response = input().strip()
		while (response != "1") and (response != "0") and (response != "2"):
			printwSpacing("Would you like the text to sound like a combination (2), a specific party (1), or only this user (0)?")
			print(divider)
			print()
			response = input().strip()
			print()
		
		if response == "2": # combination
			print()
			printwSpacing("Please input a user on the list.")
			print()
			response = input().strip()
			while response not in models:
				printwSpacing("Please input a user on the list.")
				print(divider)
				print()
				response = input().strip()
				print()
			generate(response)
			print()
		if response == "1": # party
			print()
			printwSpacing("Please choose Republican (R) or Democrat (D).")
			response = input().strip()
			while response != "R" and response != "D":
				printwSpacing("Please choose Republican (R) or Democrat (D).")
				print(divider)
				print()
				response = input().strip()
				print()
			generateParty(response)
			print()
		if response == "0": # single user
			print()
			printwSpacing("Please input a user on the list.")
			print()
			response = input().strip()
			while response not in models:
				printwSpacing("Please input a user on the list.")
				print(divider)
				print()
				response = input().strip()
				print()
			generateUser(response)
			

	if response == "0":
		print()
		printwSpacing("Please enter a valid Twitter username.")
		user = input().strip()
		addNewUser(user)
		trainAll()
		while user not in models:
			print()
			prinwSpacing("Please enter a valid Twitter username.")
			user = input().strip()
			addNewUser(user)
		print()
		printwSpacing("Would you like the text to sound like a combination (1) or only this user (0)?")
		print()
		response = input().strip()
		while response != "1" and response != "0":
			printwSpacing("Would you like the text to sound like a combination (1) or only this user (0)?")
			print(divider)
			print()
			response = input().strip()
			print()
		if response == "1":
			generate(user)
		if response == "0":
			generateUser(user)
	

while True:
	parseInput()
