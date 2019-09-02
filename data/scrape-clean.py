import twint
import csv

# Users to scrape Tweets from
usernames = ["BarackObama", "HillaryClinton", "AOC", "SenSanders", "realDonaldTrump", "MittRomney", "senatemajldr", "benshapiro"]


def scrape(user):
	""" Scrapes Tweets from given Twitter account """
	
	c = twint.Config()
	
	# Configuration/customization
	c.Username = user
	c.Limit = 500
	c.Filter_retweets = True
	c.Store_csv = True
	c.Links = "exclude"
	
	# Sets name of file and scrapes
	filename = user + ".csv"
	c.Output = filename
	twint.run.Search(c)


def clean(user):
	""" Moves Tweets to new .csv file """
	
	input  = str(user) + ".csv"
	output = str(user) + "_cleaned.csv"
	
	# Creates output .csv file
	with open(output, "w", newline = "", encoding = "utf-8") as output:
		filewriter = csv.writer(output)
		# Opens input .csv file, skips header 
		with open(input, "r", encoding = "utf-8") as input:
			pointreader = csv.reader(input)
			next(pointreader)
			# Moves Tweets from input to output
			for row in pointreader:
				filewriter.writerow([row[10]])

	
def scrape_clean():	
	""" Combines scrape and clean functions """
	for user in usernames:
		scrape(user)	
		try:
			clean(user)
		except IndexError:
			pass


scrape_clean()