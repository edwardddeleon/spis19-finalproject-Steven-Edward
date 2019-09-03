import random
import csv
import os

weights = {
	"BarackObama": {1: []},
	"HillaryClinton": {1: []}, 
	"AOC": {1: []}, 
	"SenSanders": {1: []}, 
	"realDonaldTrump": {1: []}, 
	"MittRomney": {1: []}, 
	"senatemajldr": {1: []}, 
	"benshapiro": {1: []}
#	"test": {1: []},
#	"test1": {1: []}
}


# word bank of all users combined
dict = {}

def train(user):
	input_file = str(user) + "_cleaned.csv" # sets filename which should be opened
	cwd = os.getcwd() # gets current working directory
	with open(os.path.join(cwd, "data", input_file), "r", encoding = "utf-8-sig") as input: # 
		pointreader = csv.reader(input)
		for row in pointreader:
			string = row[0].split(" ")
			counter = 0
			for word in string:
				if len(string) == 1:
					dict[string[counter]] = [string[0]]
					pass
				if counter == len(string) - 1:
					if word not in dict:
						dict[string[counter]] = [string[0]]
						pass
					else:
						dict[word].append(string[0])
						pass
				elif word in dict:
					dict[word].append(string[counter + 1])
					counter += 1
				else:
					dict[string[counter]] = [string[counter + 1]]
					counter += 1
	return dict

# loops whatever for the user's value in weights
for user in weights:
	for weight in weights[user]:
		for x in range(weight):
			dict = train(user)

def generate(model, firstWord, numWords):
    output = [firstWord]
    for key in range(numWords - 1):
        value = model.get(firstWord)
        nextWord = random.choice(value)
        output.append(nextWord)
        firstWord = nextWord
    generatedText = " ".join(output)
    return generatedText

print(dict)
test = generate(dict, "Is", 100)
print(test)