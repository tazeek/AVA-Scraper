# REFERENCE: https://github.com/sergeyk/vislab/blob/master/vislab/datasets/ava.py

from bs4 import BeautifulSoup
import urllib.request
import requests
import re

# AVA-related variables
AVA_LAST_ID = 958297
AVA_URL_FOR_ID = 'http://www.dpchallenge.com/image.php?IMAGE_ID={}'

def extractPage(url):

	# Load using requests
	requests_gallery = requests.get(url)

	# HTML Extraction using BeautifulSoup
	page_extract = BeautifulSoup(requests_gallery.text, 'lxml')

	return page_extract

def getRatings(url):

	# The ratings should be in a JSON file
	ratings_json = {}

	# Extract using BeautifulSoup
	soup_ratings = extractPage(url)

	# Extract tables from the page
	# NOTE: 'Photograph Information' will ALWAYS be extracted (Index 0)
	# If a photograph has statistics, the array will be a size of 2
	tbls = soup_ratings.findAll(
		lambda tag:
		'width' in tag.attrs and
		'cellpadding' in tag.attrs and
		tag.attrs['width'] == '750'
	)

	# Return 'None' if no statistic table found
	if len(tbls) < 1:
		return None

	# Extract ratings from the table
	ratings_array = [float(b.next_sibling) for b in tbls[1].findAll('b') if 'Avg' in b.text]

	# If there are no ratings, it means the image was disqualified
	if len(ratings_array) == 0:
		return None
	
	ratings_json['all'] = ratings_array[0]
	ratings_json['commenters'] = ratings_array[1]
	ratings_json['participants'] = ratings_array[2]
	ratings_json['non-participants']= ratings_array[3]

	return ratings_json

def getComments(url):

	# Comments are to be stored in an array
	image_comments = []

	# Extract page using BeautifulSoup
	soup_comments = extractPage(url)

	# Comments are in table format
	cmmts_tbls = soup_comments.findAll(
		lambda tag:
		'cellspacing' in tag.attrs and
		'cellpadding' in tag.attrs and
		tag.attrs['cellspacing'] == '0' and
		tag.attrs['cellpadding'] == '4'
	)

	# Loop over table by table
	for table in cmmts_tbls:

		# Extract the row, followed by the row's data
		row_data = table.find('tr').find('td')

		# Check if there is a table in the row (Ex. Replies to another comment)
		# If there is, delete it
		if row_data.find('table'):
			for table in row_data.findAll('table'):
				table.extract()
			
		print(row_data.text)
		
		print("\n\n")
	exit()

	return image_comments

def getImageURL(url):

	# Extract using BeautifulSoup
	soup_image = extractPage(url)

	# Extract images
	imgs = soup_image.findAll(
        lambda tag:
        'alt' in tag.attrs and
        'src' in tag.attrs and
        'style' in tag.attrs and
        tag.attrs['src'].startswith('http://images.dpchallenge.com/') and
        tag.attrs['src'].find('thumb') < 0
    )

	# The page displays the 50 latest images (For 'Recently Uploaded')
	# The latest (or only) image is always at index 0
	# NOTE: If no images are found, return None and handle the case
	if len(imgs) == 0:
		return None

	image_link = imgs[0]['src']

	return image_link

def getMetadata(url):

	# Meta data is to be stored in a json format
	challenge_json = {}
	semantic_json = {}

	# Extract using BeautifulSoup
	soup_meta = extractPage(url)

	# Extract Challenge ID
	challenge = soup_meta.find(
		lambda tag:
		'href' in tag.attrs and
		tag.attrs['href'].startswith('/challenge_results.php')
	)

	# Store the challenge ID in the format 'ID: Challenge Name'
	challenge_name = challenge.text
	challenge_id = int(re.findall('\d+', challenge['href'])[0])
	challenge_json[challenge_id] = challenge_name

	# Extract Semantic Tags
	semantic_tags = soup_meta.findAll(
		lambda tag:
		'href' in tag.attrs and
		tag.attrs['href'].startswith('/photo_gallery.php')
	)

	for tag in semantic_tags:

		semantic_name = tag.text
		semantic_id = int(re.findall('\d+', tag['href'])[0])

		semantic_json[semantic_id] = semantic_name

	return image_meta

def getLatestImageID(url):

	# Get the ID
	latest_image_link = getImageURL(url)

	# Split the URL string via '/'
	# The image ID is in the last index of the split link
	latest_image_id = latest_image_link.split('/')[-1]

	# Extract the ID
	latest_image_id = re.findall('\d+', latest_image_id)[0]

	return int(latest_image_id)

def scraping():

	# Get the latest Image ID from DPChallenge
	latest_image_id = getLatestImageID('http://www.dpchallenge.com/photo_browse.php?view=recentlyuploaded')
	dummy = 'http://www.dpchallenge.com/image.php?IMAGE_ID=106'

	#image_link = getImageURL(dummy)
	image_comments = getComments(dummy)
	#image_ratings = getRatings(dummy)
	#image_meta = getMetadata(dummy)


	#if image_link is not None:

	#	FILEPATH = 'AVA 2.0 Images/1201649.jpg'
	#	urllib.request.urlretrieve(image_link, FILEPATH)
	#print(image_link)

	'''
	for image_id in range(10+1, 20+1):

		# Get the image page URL
		url = AVA_URL_FOR_ID.format(image_id)

		# Get the image link
		image_link = getImageURL(url)

		# Get image ratings
		image_ratings = getRatings(url)

		# Get image comments
		image_comments = getComments(url)

		# Get image metadata
		image_meta = getMetadata(url)


		if image_link is not None:

			# Specify filepath
			FILEPATH = 'AVA 2.0 Images/' + str(image_id) + '.jpg'

			# To download save images
			urllib.request.urlretrieve(image_link, FILEPATH)
	'''

# Scraping starts here
scraping()