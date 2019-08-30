import twint
import csv
from ftfy import fix_encoding

#def scrapeAccTweets(lat, lon, km):
#	c.Geo = (str(lat) + "," + str(lon) + "," + str(km) + "km")

usernames = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # placeholder
	
def scrape_tweets(username):
	""" Scrapes Tweets from given Twitter account """
	
	c = twint.Config()
	c.Username = username
	c.Limit = 1000
	c.Filter_retweets = True
	c.Store_csv = True
	filename = username + ".csv"
	c.Output = filename
	
	twint.run.Search(c)

def fix_move(username):
	""" Fixes broken encoding and moves data to new .csv file """
	filename = username + ".csv"
	csv.reader

for user in usernames:
	scrape_tweets(user)
	fix_move(user)

#test  = "Itâ€™s why Iâ€™ve always made it a priority â€“ from my 2008 campaign until now."
#print(fix_encoding(test))
# prints "It’s why I’ve always made it a priority – from my 2008 campaign until now."