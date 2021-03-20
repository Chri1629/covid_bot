import requests
import csv, re
#import pandas as pd

def scrape(force = False):

    page_prov = requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
    page_reg = requests.get("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")

    # split the long string into a list of lines
    data_p = page_prov.content.decode('utf-8').splitlines()
    data_r = page_reg.content.decode('utf-8').splitlines()
    
    # control if length of data are higher (for regions)
    if not force:
        n_rows = 0
        with open("data/dati_regioni.csv", "r", encoding = "utf-8") as csv_file:
            n_rows = len(csv_file.readlines())
        
        print(f"Controllo righe nuove {n_rows}")
        print(f"Controllo righe vecchie {len(data_r)}")
    # if length == then no update has done
        if len(data_r) == n_rows:
            return False
       
    with open("data/dati_province.csv", "w", encoding = "utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter = ",")
        for line in data_p:
            l = re.split(',', line)
            if len(l) > 11:
                l = l[:11]
            writer.writerow(l)

    with open("data/dati_regioni.csv", "w", encoding = "utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter = ",")
        for line in data_r:
            l = re.split(',', line)
            if len(l) > 21:
                l = l[:21]
            
            writer.writerow(l)
            
    return True
