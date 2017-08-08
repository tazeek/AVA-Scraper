from bs4 import BeautifulSoup
from os import listdir

import requests
import time
import re
import pickle

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

# Split between two text files
def saveTextFiles():

	# Image ID List
	image_id_list = []

	# Specify Image path
	PATH = 'AVA 2.0 Images/'

	# Load the AVA 2.0 folder and get all the images
	image_list = [images for images in listdir(PATH)]
	
	# Remove .jpg ending
	for images in image_list:

		# After cleaning, store in list
		id = re.sub('.jpg','', images)
		image_id_list.append(id)

	# Split between two halves
	first_half = image_id_list[:len(image_id_list)//2]
	second_half = image_id_list[len(image_id_list)//2:]

	# Save each half into text file using pickle
	with open("first_half.txt", "wb") as fh:
		pickle.dump(first_half, fh)

	with open("second_half.txt", "wb") as sh:
		pickle.dump(second_half, sh)

saveTextFiles() 