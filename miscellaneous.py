from bs4 import BeautifulSoup

import urllib.request
import requests
import re
import time

# If the scraper crashes, set this variable to True
EMERGENCY = True

# Page extract
def extractPage(url):

	# Define header
	headers = {
    	'User-Agent': 'Tazeek',
    	'From': 'tazeek.rakib@gmail.com'  # This is another valid field
	}

	# Load using requests
	requests_page = requests.get(url, headers=headers)

	# Sleep for a minute
	print("SLEEPING NOW (60 seconds)")
	print(time.strftime("%H:%M:%S"),"\n")
	time.sleep(60)

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

# Scrape the gallery page for semantic tags
def scrapeGalleryPage(url):

	# Scrape using BeautifulSoup
	gallery_page = extractPage(url)

	# Dictionary to store tags
	new_semantic_dict = {}

	# Find all the rows of galleries
	gallery_rows = gallery_page.findAll(
		lambda tag:
		'width' in tag.attrs and
		'cellspacing' in tag.attrs and
		'cellpadding' in tag.attrs and
		tag.attrs['width'] == '100%' and
		tag.attrs['cellspacing'] == '0' and
		tag.attrs['cellpadding'] == '3'
	)[0].findChildren('td')

	# Loop over row by row
	for row in gallery_rows:
		
		# Extract all links for a row
		gallery_links = row.findAll(
			lambda tag:
			'href' in tag.attrs and
			tag.attrs['href'].startswith('/photo_gallery.php?')
		)

		# Loop over link by link
		for gallery in gallery_links:

			# Extract ID
			tag_id = int(re.findall('\d+', gallery['href'])[0])

			# Extract text
			tag_name = gallery.text.replace(' ','_')

			# Store in key-value format ('ID': 'Name')
			new_semantic_dict[tag_id] = tag_name

	# Save in a text file
	with open('AVA 2.0 Semantics.txt', 'w', encoding='utf-8') as outfile:
		for key, value in new_semantic_dict.items():
			outfile.write(str(key) + ' ' + value + "\n")

# Scrape the challenge page (ALL results)
def scrapeChallengePage(url, stop_id):

	# Scrape using BeautifulSoup
	challenge_page = extractPage(url)

	# JSON File
	new_challenge_dict = {}

	# Number of pictures and comments
	pictures_new = 0
	comments_new = 0

	'''
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
	'''
	'''
	# Add in the entries (Rough idea of new photographs)
	# This area can be used for metadata purposes
	challenge_rows = challenge_page.findAll(
		lambda tag:
		'id' in tag.attrs and
		tag.attrs['id'] == 'challenges'
	)[1].findChildren('tr')

	challenge_rows.pop(0)

	for i,row in enumerate(challenge_rows):

		# Number of new challenges are 1080
		if i == 1080:
			break
		
		# Find metadata		
		row_td = row.findChildren('td', {'align': 'center'})

		# Add in number of new pictures and comments
		pictures_new += int(row_td[0].text)
		comments_new += int(row_td[7].text.replace(',',''))

	print(pictures_new)
	print(comments_new)
	'''

	return

# Cases where scraper crashes unexpectedly
def emergencyCase():

	# Find last line
	last_line = ''

	# Read the last line of 'AVA 2.0' text file
	with open('AVA 2.0.txt') as file:
		last_line = list(file)[-1].split()

	# Get the last index number
	last_index = last_line[0]

	# Get the last image id scraped
	last_image_id = last_line[1]

	# Get the last challenge id scraped/scraping
	last_challenge_id = last_line[-1]

	return last_index, last_image_id, last_challenge_id

# Create URL for Image downlad:
def createImageURL(challenge_id, image_id):

	# Create the URL archive link
	image_url = 'http://images.dpchallenge.com/images_challenge/'

	# Get the challenge range with challenge id
	if challenge_id >= 2000:
		challenge_range = '2000-2999/' 
	else:
		challenge_range = '1000-1999/'

	image_url += challenge_range + str(challenge_id) + '/1200/'

	# Add in the image id
	image_url += 'Copyrighted_Image_Reuse_Prohibited_' + image_id + '.jpg'

	return image_url

def extractImages(EMERGENCY):

	# Load the challenge IDs from the AVA 2.0
	new_challenge_list = []
	count = 0

	with open('AVA 2.0 challenges.txt') as file:
		for line in file:
			challenge_data = line.split()
			new_challenge_list.append(challenge_data[0])

	# In case of emergency, load everything from scratch
	if EMERGENCY:
		
		# Get challenge id, image id, and index number
		count, image_id, challenge_id = emergencyCase()

		# Get index of challenge scraped (Perform manual inspection)
		last_challenge_index = new_challenge_list.index(challenge_id)

		# Slice the array
		new_challenge_list = new_challenge_list[last_challenge_index:]

	print("LAST INDEX: ", count)
	print("LAST IMAGE ID: ", image_id)
	print("LAST CHALLENGE_ID: ", challenge_id)
	print("INDEX ID: ", new_challenge_list.index(challenge_id))

	print("\n", new_challenge_list)
	
	exit()

	# Create URL variable to navigate challenge pages (Dummy test: 2497)
	full_challenge_url = 'http://dpchallenge.com/challenge_results.php?CHALLENGE_ID={}&show_full=1'

	for i,challenge_id in enumerate(new_challenge_list):

		url = full_challenge_url.format(challenge_id)

		# Extract page using BeautifulSoup
		full_challenge_page = extractPage(url)

		# Progress output
		print("EXTRACTION PROGRESS: %d/%d" % (i+1, len(new_challenge_list)))
		print("Current ID extracting: ", challenge_id)
		print (time.strftime("%H:%M:%S"))
		print("\n\n")

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
		for row in image_rows:
		
			row_td = row.findChildren('td')
		
			# Extract ratings data (Ignore the first entry as it corresponds to position)
			ratings = [b.text for b in row_td[1].findAll('b') if 'N/A' not in b.text][1:]

			# If the photograph doesn't have 4 ratings, exclude it
			if len(ratings) == 4: 

				# Extract number of votes
				vote = [b.text for b in row_td[1].findAll('span')][-1]

				# Extract Image ID
				image_id = row_td[0].find('a')['href']
				image_id = int(re.findall('\d+', image_id)[0])

				# Create Image URL 
				image_url = createImageURL(int(challenge_id), str(image_id))

				# Concat the necessary data for given image's ratings
				image_data = [str(count+1), str(image_id)] + ratings + [challenge_id]
				image_data = (' '.join(image_data)) + '\n'

				# Concat the necessary data for the image's votes
				image_vote_data = ' '.join([str(count+1), str(image_id), vote]) + '\n'
				count += 1

				# Store in images in AVA 2.0 folder
				FILEPATH = 'AVA 2.0 Images/' + str(image_id) + '.jpg'
				urllib.request.urlretrieve(image_url, FILEPATH)

				# Append ratings to 'AVA 2.0' text file
				with open("AVA 2.0.txt", "a") as append_file:
					append_file.write(image_data)

				# Append votes to 'AVA 2.0 Votes' text file
				with open('AVA 2.0 Votes.txt', 'a') as append_file:
					append_file.write(image_vote_data)

				print("IMAGES EXTRACTED: %s/%s" % (str(count+1), '82702'))


		print("\n")

	return

# Get the last ID
#ava_last_id = getLastChallenge()

# Scrape Challenge Page
#url = 'http://dpchallenge.com/challenge_history.php?order_by=0d&open=1&member=1&speed=1&invitational=1&show_all=1'
#scrapeChallengePage(url, ava_last_id)

# Scrape Gallery Page
#url = 'http://dpchallenge.com/photo_gallery.php'
#scrapeGalleryPage(url)

# Scrape Images from each challenge (DEPLOY IT IN PC)
extractImages(EMERGENCY)