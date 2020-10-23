from plot.positivi_vs_tamponi import positivi_tamponi
from plot.tamponi import tamponi
from plot.terapia_intensiva import terapia_intensiva
from plot.casi import casi
from plot.morti import morti


def plot_producer():
    print("PRODUCING PLOTS")
    positivi_tamponi()
    tamponi()
    terapia_intensiva()
    casi()
    morti()
    print("PLOT PRODUCED")
