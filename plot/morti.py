import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def morti():
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))

    fig = plt.figure(figsize = (6,4))
    plt.plot(date, raggruppati['deceduti'].diff(), color = "skyblue", alpha = 1)
    plt.scatter(x = max(date), y = raggruppati['deceduti'].diff().tail(1), 
        label = "Ultimo valore {}".format(int(raggruppati['deceduti'].diff().tail(1).values[0])))
    plt.hlines(y = raggruppati['deceduti'].diff().max(), xmin=0,xmax=max(date), label="Picco massimo")
    plt.xlim(left = 0)
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Morti", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Nuove morti per giorno in Italia", size = 15)
    plt.legend()
    plt.grid()
    plt.savefig("pics/morti/nuovi_morti.png", dpi = 100)
    plt.close(fig)

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['deceduti']
        fig = plt.figure(figsize = (6,4))
        plt.plot(date, per_regioni.diff(), color = "skyblue", alpha = 1)
        plt.scatter(x = max(date), y = per_regioni.diff().tail(1), 
        label = "Ultimo valore {}".format(int(per_regioni.diff().tail(1).values[0])))
        plt.xlim(left = 0)
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi morti", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Nuovi morti al giorno in {}".format(regione), size = 15)
        plt.grid()
        plt.legend()
        fig.savefig("pics/morti/nuovi_morti_{}.png".format(regione), dpi = 100)
        plt.close(fig)