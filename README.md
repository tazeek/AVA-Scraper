# AVA-Scraper

---
## What is AVA?

**AVA: A Large-Scale Database for Aesthetic Visual Analysis**

The AVA dataset was released in 2012 for conducting research on image aesthetics. The dataset consists of over 250,000 images.
The images consists of number of votes for ratings (1-10), semantic tags, and the challenges it is associated to.
PAPER: **[AVA: A Large-Scale Database for Aesthetic Visual Analysis](http://refbase.cvc.uab.es/files/MMP2012a.pdf)**

Later in 2016, the comments (labeled as AVA-Comments) were released for the respective images and consists of over 1.5 million comments.
PAPER: **[Joint Image and Text Representation for Aesthetics Analysis](http://infolab.stanford.edu/~wangz/project/imsearch/Aesthetics/ACMMM2016/zhou.pdf)**

Both comments and images were taken from [dpchallenge.com](dpchallenge.com).

---
## What is AVA-Scraper?

Images after 2012 are not scraped and are still available on dpchallenge.com. This scraper is used to download the images, comments and other metadata. It is divided into **three** parts:

- [Image scraper](https://github.com/tazeek/AVA-Scraper/blob/master/image_scraper.py): Used for extracting images, their ratings, and number of votes. Stored as IMAGE_ID.jpg

- [Comment scraper](https://github.com/tazeek/AVA-Scraper/blob/master/comment_scraper.py): Used for extracting comments from images, some text cleaning (example: removal of URLs, carraige returns character, etc) and storage. Stored as IMAGE_ID.txt, with one line per comment.

- [Others](https://github.com/tazeek/AVA-Scraper/blob/master/other_scraper.py): Used for extracting new challenges and existing rules