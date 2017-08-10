from utils import extractPage

from bs4 import BeautifulSoup

import re
import pickle
import itertools
import codecs

# Variables in cases of emergency
# NOTE: When using PC, use 'first_half.txt' and for laptop, use 'second_half.txt'
EMERGENCY = True
FILE = 'second_half.txt'

def emergencyCase():

	# Find last line
	last_line = ''

	# Read the last line of 'AVA 2.0' text file
	with open('AVA 2.0 Image Semantics.txt') as file:
		last_line = list(file)[-1].split()

	# Get the last image id scraped
	last_image_id = last_line[0]

	return last_image_id

def cleanComments(comments):

	clean_comments = []

	for comment in comments:

		# Extract again (JUST IN CASE)
		comment = BeautifulSoup(comment, "lxml").get_text()

		# Some comments are edited and the datastamp of edited message is extracted
		comment = re.sub(r"Message edited by author .*", '', comment)

		# Some comments have urls
		comment = re.sub(r'^https?:\/\/.*[\r\n]*', '', comment, flags=re.MULTILINE)

		# Word Standardizing (Ex. Looooolll should be Looll)
		comment = ''.join(''.join(s)[:2] for _, s in itertools.groupby(comment))

		# Remove Encodings
		comment = re.sub(r'\\\\', r'\\', comment)
		comment = re.sub(r'\\', ' ', comment)
		comment = re.sub(r'\\x\w{2,2}',' ', comment)
		comment = re.sub(r'\\u\w{4,4}', ' ', comment)
		comment = re.sub(r'\\n', '.', comment)

		# Remove carraige returns character
		comment = ' '.join(comment.splitlines())

		#Remove Unicode characters
		comment = codecs.decode(comment, 'unicode-escape')
		comment = ''.join([i if ord(i) < 128 else '' for i in comment])

		clean_comments.append(comment)

	return clean_comments


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
		
		# Append the cleaned comment
		image_comments.append(comment)

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

def scraping(EMERGENCY, FILE):

	# AVA Image URL and text file
	AVA_URL_FOR_ID = 'http://www.dpchallenge.com/image.php?IMAGE_ID={}'
	TEXT_FILE_DIR = 'AVA 2.0 Comments/{}.txt' 

	# Load Pickle file
	with open(FILE,'rb') as fh:
		image_id_list = pickle.load(fh)

	# In case of emergency, load everything from scratch
	if EMERGENCY:

		# Get image id of the last image scraped
		last_image_id = emergencyCase()

		# Get index of the last image and move to next index
		last_image_index = image_id_list.index(last_image_id) + 1

		# Slice the array
		image_id_list = image_id_list[last_image_index:]

	for i,image_id in enumerate(image_id_list):

		# Get the image page URL and the text file
		url = AVA_URL_FOR_ID.format(image_id)
		file = TEXT_FILE_DIR.format(image_id)

		# Extract Page
		page_extract = extractPage(url)

		# Get image metadata
		image_meta = [image_id] + getMetadata(page_extract)

		# Store image meta in string: 'ID, Tag_IDs'
		image_meta = ' '.join(image_meta) + '\n'

		# Get image comments
		image_comments = getComments(page_extract)

		# Clean image comments
		clean_comments = cleanComments(image_comments)

		# Store in 'Image_ID.txt'. One line = One comment
		with open(file, 'w') as write_file:
			for comment in clean_comments:
				write_file.write(comment + '\n')

		# Append to 'AVA 2.0 Semantics'
		with open('AVA 2.0 Image Semantics.txt', 'a') as append_file:
			append_file.write(image_meta)

		print("\n\nEXTRACTION PROGRESS: %d/%d \n\n" % (i+1, len(image_id_list)))

	return

# Scraping starts here
scraping(EMERGENCY, FILE)