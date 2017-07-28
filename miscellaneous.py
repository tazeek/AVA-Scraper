#from scraper import extractPage

import urllib.request
import requests
import re
import time

# Get the latest challenge number from AVA 1.0
def getLastChallenge():

	# Last challenge to be stored in this variable
	last_challenge_id = None

	# Read the text file
	with open('challenges.txt') as file:

		# 1 line = Challenge ID followed by Challenge Name
		for line in file:
			challenge_info = line.split()

			# Compare with current number
			if (last_challenge_id is None) or (last_challenge_id < int(challenge_info[0])):
				last_challenge_id = int(challenge_info[0])

	return last_challenge_id

# Scrape the challenge page (ALL results)
def scrapeChallengePage(url):

	# Scrape using BeautifulSoup

	# Find all rows (Each row is one challenge)

	# Loop challenge by challenge 

	# Extract ID

	# If ID matches the last challenge of AVA 1.0, break

	# Save in json format ('ID':'Challenge Name')

	# Add in the entries (Rough idea of new photographs)

	return

getLastChallenge()