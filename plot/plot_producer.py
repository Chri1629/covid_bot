from plot.positivi_vs_tamponi import positivi_tamponi
from plot.tamponi import tamponi
from plot.terapia_intensiva import terapia_intensiva
from plot.casi import casi
from plot.morti import morti
from plot.ricoverati import ricoverati
from plot.guariti import guariti
from plot.vaccini import vaccini, vaccini_cum, vaccini_fasce, vaccini_reg, vaccini_fasce_perc
from pathlib import Path


def plot_producer():
    
    Path("pics/rapporto_tamponi").mkdir(parents=True, exist_ok=True)
    Path("pics/rapporto_tamponi_news").mkdir(parents=True, exist_ok=True)
    positivi_tamponi()
    
    Path("pics/tamponi").mkdir(parents=True, exist_ok=True)
    Path("pics/tamponi_news").mkdir(parents=True, exist_ok=True)
    tamponi()
    
    Path("pics/terapia").mkdir(parents=True, exist_ok=True)
    Path("pics/terapia_news").mkdir(parents=True, exist_ok=True)
    terapia_intensiva()
    
    Path("pics/nuovi_positivi").mkdir(parents=True, exist_ok=True)
    Path("pics/nuovi_positivi_news").mkdir(parents=True, exist_ok=True)
    casi()
    
    Path("pics/morti").mkdir(parents=True, exist_ok=True)
    Path("pics/morti_news").mkdir(parents=True, exist_ok=True)
    morti()
    
    Path("pics/guariti").mkdir(parents=True, exist_ok=True)
    Path("pics/guariti_news").mkdir(parents=True, exist_ok=True)
    guariti()
    
    Path("pics/ricoverati").mkdir(parents=True, exist_ok=True)
    Path("pics/ricoverati_news").mkdir(parents=True, exist_ok=True)
    ricoverati()
    
    # plot vaccini
    Path("pics/vaccini").mkdir(parents=True, exist_ok=True)
    Path("pics/vaccini/day").mkdir(parents=True, exist_ok=True)
    Path("pics/vaccini/cum").mkdir(parents=True, exist_ok=True)
    vaccini()
    vaccini_cum()
    vaccini_fasce()
    vaccini_fasce_perc()
    #vaccini_reg()
    
    pass
