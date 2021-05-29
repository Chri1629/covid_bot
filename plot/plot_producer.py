from plot.positivi_vs_tamponi import positivi_tamponi
from plot.tamponi import tamponi
from plot.terapia_intensiva import terapia_intensiva
from plot.casi import casi
from plot.morti import morti
from plot.ricoverati import ricoverati
from plot.guariti import guariti
from plot.vaccini import vaccini, vaccini_cum, vaccini_fasce, vaccini_reg



def plot_producer():
    #print("PRODUCING PLOTS")
    positivi_tamponi()
    tamponi()
    terapia_intensiva()
    casi()
    morti()
    guariti()
    ricoverati()
    # plot vaccini
    vaccini()
    vaccini_cum()
    vaccini_fasce()
    vaccini_reg()
    #print("PLOT PRODUCED")
    pass
