import twint

def scrapeAccTweets(lat, lon, km):
	c = twint.Config()
	c.Geo = (str(lat) + "," + str(lon) + "," + str(km) + "km")
	c.Limit = 5000
	c.Lang = "en"
	c.Filter_retweets = False
	c.Store_csv = True
	c.Output = "location.csv"
	twint.run.Search(c)
	
def scrapeAccTweets(username):
	c = twint.Config()
	c.Username = str(username)
	c.Limit = 1000
	c.Filter_retweets = True
	
	c.Store_csv = True
	filename = str(username) + ".csv"
	c.Output = filename
	
	twint.run.Search(c)
