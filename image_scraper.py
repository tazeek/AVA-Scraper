from utils import extractPage

from bs4 import BeautifulSoup

import urllib.request
import requests
import re
import time

# If the scraper crashes, set this variable to True
EMERGENCY = True

# Cases where scraper crashes unexpectedly
def emergencyCase():

	# Find last line
	last_line = ''

	# Read the last line of 'AVA 2.0' text file
	with open('AVA 2.0.txt') as file:
		last_line = list(file)[-1].split()

	# Get the last index number
	last_index = int(last_line[0])

	# Get the last image id scraped
	last_image_id = int(last_line[1])

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
		count, last_image_id, challenge_id = emergencyCase()

		# Get index of challenge scraped (Perform manual inspection)
		last_challenge_index = new_challenge_list.index(challenge_id)

		# Slice the array
		new_challenge_list = new_challenge_list[last_challenge_index:]

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

		# Extract the rows
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

				# In case of emergency, execute this
				if EMERGENCY:

					# Check if the current id matches the last id
					# If it does, emergency case stops
					if image_id == last_image_id:
						EMERGENCY = False
						continue
					else:
						continue

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

# Scrape Images from each challenge (DEPLOY IT IN PC)
extractImages(EMERGENCY)