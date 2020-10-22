from preprocessing.scraper import scrape
from preprocessing.fixer_data import fix_datasets
from plot.casi import casi
from plot.morti import morti

if __name__ == "__main__":
    print("SCRAPING UPDATED DATASETS ...")
    #scrape()
    print("Dataset dowloaded")
    print("FIXING DATASETS ...")
    #fix_datasets()
    print("All done!")
    #casi()
    morti()
    