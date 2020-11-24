from .fixer_data import fix_datasets
from .scraper import scrape

def preprocess_data():
    print("SCRAPING THE DATA")
    flag = scrape()
    if (flag):
       print("DATA DOWNLOADED")
       fix_datasets()
       print("DATA FIXED")
       return True
    else:
       print("DATA NOT DOWNLOADED - no update found")
       return False