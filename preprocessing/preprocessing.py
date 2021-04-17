from .fixer_data import fix_datasets
from .scraper import scrape
from .scraper import scrape_vaccini

def preprocess_data(force = False):
    #print("SCRAPING THE DATA")
    flag = scrape(force)
    if (flag):
       #print("DATA DOWNLOADED")
       fix_datasets()
       #print("DATA FIXED")
       return True
    else:
       #print("DATA NOT DOWNLOADED - no update found")
       return False
   #scrape_vaccini(force)