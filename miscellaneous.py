from bs4 import BeautifulSoup

import urllib.request
import requests
import re
import time

# Page extract
def extractPage(url):

	# Define header
	headers = {
    	'User-Agent': 'Tazeek',
    	'From': 'tazeek.rakib@gmail.com'  # This is another valid field
	}

	# Load using requests
	requests_page = requests.get(url, headers=headers)

	# HTML Extraction using BeautifulSoup
	page_extract = BeautifulSoup(requests_page.text, 'lxml')

	return page_extract

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
def scrapeChallengePage(url, stop_id):

	# Scrape using BeautifulSoup
	challenge_page = extractPage(url)

	# JSON File
	new_challenge_dict = {}

	# Number of pictures 
	pictures_new = 0

	# Find all rows (Each row is one challenge)
	challenge_rows = challenge_page.findAll(
		lambda tag:
		'href' in tag.attrs and
		tag.attrs['href'].startswith('/challenge_results.php')
	)


	# Loop challenge by challenge 
	for row in challenge_rows:

		# Extract ID
		row_id = int(re.findall('\d+', row['href'])[0])

		# If ID matches the last challenge of AVA 1.0, break
		if row_id == stop_id:
			break

		# Extract Challenge name (Replace spaces with _)
		row_name = row.text.split()
		row_name = "_".join(row_name)

		# Save in json format ('ID':'Challenge Name')
		new_challenge_dict[row_id] = row_name

	# Save in a text file
	with open("AVA 2.0 challenges.txt", "w", encoding='utf-8') as outfile:
		for key, value in new_challenge_dict.items():
			outfile.write(str(key) + " " + value + "\n")

	# Add in the entries (Rough idea of new photographs)
	# This area can be used for metadata purposes
	challenge_rows = challenge_page.findAll(
		lambda tag:
		'id' in tag.attrs and
		tag.attrs['id'] == 'challenges'
	)[1].findChildren('tr')

	challenge_rows.pop(0)

	for i,row in enumerate(challenge_rows):

		if i == 1080:
			break
		
		row_td = row.findChildren('td', {'align': 'center'})

		print(pictures_new, row_td[0].text)
		pictures_new += int(row_td[0].text)

	print(pictures_new)
	time.sleep(60)

	return

def extractImages():

	# Load the challenge IDs from the AVA 2.0
	new_challenge_list = []

	with open('AVA 2.0 challenges.txt') as file:
		for line in file:
			challenge_data = line.split()
			new_challenge_list.append(challenge_data[0])

	# Create URL variable to navigate challenge pages (Dummy test: 2497)
	full_challenge_url = 'http://dpchallenge.com/challenge_results.php?CHALLENGE_ID={}&show_full=1'
	full_challenge_url = full_challenge_url.format('2330')

	# Extract page using BeautifulSoup
	full_challenge_page = extractPage(full_challenge_url)

	# Extract the table of images from the page
	image_table = full_challenge_page.find(
		lambda tag:
		'width' in tag.attrs and
		'align' in tag.attrs and
		'cellspacing' in tag.attrs and
		'cellpadding' in tag.attrs and
		tag.attrs['align'] == 'center' and
		tag.attrs['width'] == '90%'
	)

	# Extract the rows and remove the first entry
	image_rows = image_table.findChildren('tr', {'class': 'forum-bg1'})

	# Loop row by row
	# Each row has two table data: one for image, the other for ratings
	for i,row in enumerate(image_rows):
		
		row_td = row.findChildren('td')
		
		# Extract ratings data (Ignore the first entry as it corresponds to position)
		ratings = [b.text for b in row_td[1].findAll('b') if 'N/A' not in b.text][1:]

		# If the photograph doesn't have 4 ratings, exclude it
		if len(ratings) == 4:
			print(i+1)

	# Modify the URL to get the original image

	# Store in images in AVA 2.0 folder

	time.sleep(60)
	exit()

	return

# Get the last ID
#ava_last_id = getLastChallenge()

# Scrape Challenge Page
#url = 'http://dpchallenge.com/challenge_history.php?order_by=0d&open=1&member=1&speed=1&invitational=1&show_all=1'
#scrapeChallengePage(url, ava_last_id)

# Extract Images from each challenge 
extractImages()

# Save Images and their ratings