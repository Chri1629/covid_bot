from .fixer_data import fix_datasets
from .scraper import scrape

def preprocess_data():
    print("SCRAPING THE DATA")
    scrape()
    print("DATA DOWNLOADED")
    fix_datasets()
    print("DATA FIXED")