# REFERENCE: https://github.com/sergeyk/vislab/blob/master/vislab/datasets/ava.py

from bs4 import BeautifulSoup
import urllib.request
import requests
import re

def getLatestImageID():

	# URL for recently uploaded images
	IMAGE_GALLERY_URL = 'http://www.dpchallenge.com/photo_browse.php?view=recentlyuploaded'

	# Load using requests
	requests_gallery = requests.get(IMAGE_GALLERY_URL)

	# HTML Extraction using BeautifulSoup
	soup_gallery = BeautifulSoup(requests_gallery.text, 'lxml')

	# Extract images
	imgs = soup_gallery.findAll(
        lambda tag:
        'alt' in tag.attrs and
        'src' in tag.attrs and
        tag.attrs['src'].startswith('http://images.dpchallenge.com/')
        and 'style' in tag.attrs and
        tag.attrs['src'].find('thumb') < 0
    )

	# The page displays the 50 latest images
	# The latest image is always at index 0
	image_link = imgs[0]['src']

	# Split the URL string via '/'
	# The image ID is in the last index of the split link
	latest_image_id = image_link.split('/')[-1]

	# Extract the ID
	latest_image_id = re.findall('\d+', latest_image_id)[0]

	print(latest_image_id)


# Get latest image ID
getLatestImageID()
exit()

# The last Image ID in AVA 1.0
AVA_LAST_ID = 958297

# FOR IMAGE ID
# AVA_URL_FOR_ID = 'http://www.dpchallenge.com/image.php?IMAGE_ID={}'
# dummy = 'http://www.dpchallenge.com/image.php?IMAGE_ID=1201649'

print("\n")
# Load using requests
#r = requests.get(dummy)

# Extract and, if needed for viewing, prettify
# NOTE: Every url from dpchallenge.com has information encoded in 'ISO-8859-1/latin-1'
#soup = BeautifulSoup(r.text, 'lxml')
#soup = soup.prettify('latin-1')

# Extracting the image
#imgs = soup.findAll(
#        lambda tag:
#        'alt' in tag.attrs and
#        'src' in tag.attrs and
#        tag.attrs['src'].startswith('http://images.dpchallenge.com/')
#        and 'style' in tag.attrs and
#        tag.attrs['src'].find('thumb') < 0
#    )

#print(imgs[0]['src'])
#urllib.request.urlretrieve(imgs[0]['src'], "local-filename.jpg")