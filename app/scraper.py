import argparse
from urllib.request import urlopen

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('--website', help='The website to be scraped')
args = parser.parse_args()

# website = "http://olympus.realpython.org/profiles/dionysus"
website = args.website

try:
    page = urlopen(website)
except ValueError as e:
    print("Error scraping website")
    exit()

# Find all externally loaded sources i.e. images/scripts/fonts not hosted on *website* to be scraped
# These are any html which include hrefs or src (img and script tags) and start with https:// or www.
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

externally_loaded_sources = ["img", "script"]

for scr in soup.find_all('src'):
    print(scr)
    print("------")
    print("------")
    print("------")
