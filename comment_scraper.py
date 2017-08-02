from bs4 import BeautifulSoup
from os import listdir

import urllib.request
import requests
import re
import time

def extractPage(url):

	# Define header
	headers = {
    	'User-Agent': 'Tazeek',
    	'From': 'tazeek.rakib@gmail.com'  # This is another valid field
	}

	# Load using requests
	requests_gallery = requests.get(url)

	# HTML Extraction using BeautifulSoup
	page_extract = BeautifulSoup(requests_gallery.text, 'lxml')

	return page_extract

def getComments(soup_comments):

	# Comments are to be stored in an array
	image_comments = []

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
		
		# Get the comment here
		comment = row_data.text

		# Some comments are edited and the datastamp of edited message is extracted
		comment = re.sub(r"Message edited by author .*", '', comment)

		# Some comments have urls
		comment = re.sub(r'^https?:\/\/.*[\r\n]*', '', comment, flags=re.MULTILINE)
		
		# Append the cleaned comment
		image_comments.append(comment)

	print(image_comments)

	return image_comments

def getMetadata(soup_meta):

	# Meta data is to be stored in a json format
	semantic_json = {}

	# Extract using BeautifulSoup
	soup_meta = extractPage(url)

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

	return semantic_json

def getImageID():

	# Image ids are to be stored in an array
	image_id_list = []

	# Load the AVA 2.0 folder and get all the images


def scraping():

	# AVA Image URL
	AVA_URL_FOR_ID = 'http://www.dpchallenge.com/image.php?IMAGE_ID={}'

	exit()

	for image_id in range(AVA_LAST_ID+1, latest_image_id+1):

		# Get the image page URL
		#url = AVA_URL_FOR_ID.format(image_id)

		# Extract Page
		#page_extract = extractPage(url)

		# Get image comments
		#image_comments = getComments(page_extract)

		# Get image metadata
		#image_meta = getMetadata(page_extract)

		# Delay request by 60s (see robots.txt)
		time.delay(60)

	return

# Scraping starts here
scraping()