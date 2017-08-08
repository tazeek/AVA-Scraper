from utils import extractPage

from bs4 import BeautifulSoup

import re
import pickle

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
		#comment = re.sub(r"Message edited by author .*", '', comment)

		# Some comments have urls
		#comment = re.sub(r'^https?:\/\/.*[\r\n]*', '', comment, flags=re.MULTILINE)
		
		# Append the cleaned comment
		image_comments.append(comment)

	print(image_comments)
	exit()

	return image_comments

def getMetadata(soup_meta):

	# Meta data is to be stored in a json format
	semantic_list = []

	# Extract Semantic Tags
	semantic_tags = soup_meta.findAll(
		lambda tag:
		'href' in tag.attrs and
		tag.attrs['href'].startswith('/photo_gallery.php')
	)

	# Loop tag by tag, if any
	for tag in semantic_tags:

		semantic_id = re.findall('\d+', tag['href'])[0]

		semantic_list.append(semantic_id)

	# If no tags found, add 0
	if len(semantic_list) == 0:
		semantic_list.append('0')

	return semantic_list

def scraping():

	# AVA Image URL
	AVA_URL_FOR_ID = 'http://www.dpchallenge.com/image.php?IMAGE_ID={}'

	# Load Pickle file
	with open('first_half.txt','rb') as fh:
		image_id_list = pickle.load(fh)

	for image_id in image_id_list:

		# Get the image page URL
		url = AVA_URL_FOR_ID.format(image_id)

		# Extract Page
		page_extract = extractPage(url)

		# Get image metadata
		image_meta = [image_id] + getMetadata(page_extract)

		# Store image meta in string: 'ID, Tag_IDs'
		image_meta = ' '.join(image_meta) + '\n'

		# Get image comments
		#image_comments = getComments(page_extract)

		# Clean image comments

		# Append to 'AVA 2.0 Semantics'
		#with open('AVA 2.0 Image Semantics.txt', 'a') as append_file:
		#	append_file.write(image_meta)

		exit()

	return

# Scraping starts here
scraping()