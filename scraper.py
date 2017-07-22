# REFERENCE: https://github.com/sergeyk/vislab/blob/master/vislab/datasets/ava.py

from bs4 import BeautifulSoup
import urllib.request
import requests

# FOR IMAGE ID
# AVA_URL_FOR_ID = 'http://www.dpchallenge.com/image.php?IMAGE_ID={}'
dummy = 'http://www.dpchallenge.com/image.php?IMAGE_ID=1201649'

print("\n")
# Load using requests
r = requests.get(dummy)

# Extract and, if needed for viewing, prettify
# NOTE: Every url from dpchallenge.com has information encoded in 'ISO-8859-1/latin-1'
soup = BeautifulSoup(r.text, 'lxml')
#soup = soup.prettify('latin-1')

# Extracting the image
imgs = soup.findAll(
        lambda tag:
        'alt' in tag.attrs and
        'src' in tag.attrs and
        tag.attrs['src'].startswith('http://images.dpchallenge.com/')
        and 'style' in tag.attrs and
        tag.attrs['src'].find('thumb') < 0
    )

print(imgs[0]['src'])
#urllib.request.urlretrieve(imgs[0]['src'], "local-filename.jpg")