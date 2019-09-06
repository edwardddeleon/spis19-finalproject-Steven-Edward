import markovify
import random
import csv
import os


# comment every line
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


# word bank of all users combined
dict = {}

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
		weights[account] += 0.50
	if account in affiliation:
		party = affiliation.get(account)
		for user in affiliation:
			if affiliation.get(user) == party:
				if user != account:
					weights[user] += 0.1
	for weight in weights:
		weight_list.append(weights[weight])
	for model in models:
		model_list.append(models[model])
	test = markovify.combine(model_list, weight_list)
	print(test.make_short_sentence(280))
	

def parseInput(user):
	if str(user) in models:
		generate(user)
		print(weights)
	else:
		print()
		print("Please choose one of the following usernames: ")
		print()
		for model in models:
			print(model)
	print()
	
			
trainAll()

while True:
	print("Enter a Twitter username: ")
	user = input()
	parseInput(user)