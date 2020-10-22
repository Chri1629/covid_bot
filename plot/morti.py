import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def morti():
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))

    plt.figure(figsize = (6,4))
    plt.plot(date, raggruppati['deceduti'], color = "skyblue", alpha = 1)
    plt.xlim(left = 0)
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Morti", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Nuove morti per giorno", size = 15)
    plt.grid()
    plt.savefig("pics/nuovi_morti.png", dpi = 100)

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['deceduti']
        fig = plt.figure(figsize = (6,4))
        plt.plot(date, per_regioni, color = "skyblue", alpha = 1)
        plt.xlim(left = 0)
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi morti", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Nuovi morti al giorno in {}".format(regione), size = 15)
        plt.grid()
        plt.show()
        fig.savefig("pics/nuovi_morti_{}.png".format(regione), dpi = 100)