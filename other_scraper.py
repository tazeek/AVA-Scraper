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

	# Sleep for a minute
	print("SLEEPING NOW (60 seconds)")
	print(time.strftime("%H:%M:%S"),"\n")
	time.sleep(60)

	# HTML Extraction using BeautifulSoup
	page_extract = BeautifulSoup(requests_page.text, 'lxml')

	return page_extract