# REFERENCE: https://github.com/sergeyk/vislab/blob/master/vislab/datasets/ava.py

from bs4 import BeautifulSoup
import urllib.request
import requests
import re

# Variables to specify which data (image, comments, ...) should be downloaded
DOWNLOAD_IMAGES = True
DOWNLOAD_COMMENTS = True
DOWNLOAD_RATINGS = True
DOWNLOAD_META = True

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
	
	ratings_json['all']				= ratings_array[0]
	ratings_json['commenters']		= ratings_array[1]
	ratings_json['participants']	= ratings_array[2]
	ratings_json['non-participants']= ratings_array[3]

	print(ratings_json)

	return ratings_json

def getComments(url):

	return 

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

def getLatestImageID(url):

	# Get the ID
	latest_image_link = getImageURL(url)

	# Split the URL string via '/'
	# The image ID is in the last index of the split link
	latest_image_id = latest_image_link.split('/')[-1]

	# Extract the ID
	latest_image_id = re.findall('\d+', latest_image_id)[0]

	return int(latest_image_id)

def downloadImages():

	# Get the latest Image ID from DPChallenge
	latest_image_id = getLatestImageID('http://www.dpchallenge.com/photo_browse.php?view=recentlyuploaded')
	dummy = 'http://www.dpchallenge.com/image.php?IMAGE_ID=1201649'

	#image_link = getImageURL(dummy)
	image_ratings = getRatings(dummy)

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


		if image_link is not None:

			# Specify filepath
			FILEPATH = 'AVA 2.0 Images/' + str(image_id) + '.jpg'

			# To download save images
			urllib.request.urlretrieve(image_link, FILEPATH)
	'''

# Download Images
if DOWNLOAD_IMAGES:
	downloadImages()

# FOR IMAGE ID
# 