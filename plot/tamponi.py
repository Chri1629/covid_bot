import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def tamponi():
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))

    fig = plt.figure(figsize = (6,4))
    plt.plot(date, raggruppati['tamponi'].diff(), color = "gray", alpha = 0.7)
    plt.scatter(x = max(date), y = raggruppati['tamponi'].diff().tail(1), color = "gray",
        label = "Ultimo valore: {}".format(int(raggruppati['tamponi'].diff().tail(1).values[0])))
    plt.xlim(left = 0)
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Nuovi tamponi", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Nuovi tamponi al giorno in Italia", size = 15)
    plt.legend()
    plt.grid()
    fig.savefig("pics/tamponi/tamponi.png", dpi = 100)
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['tamponi']
        fig = plt.figure(figsize = (6,4))
        plt.plot(date, per_regioni.diff(), color = "gray", alpha = 0.7)
        plt.scatter(x = max(date), y = per_regioni.diff().tail(1), color = "gray",
        label = "Ultimo valore: {}".format(int(per_regioni.diff().tail(1).values[0])))
        plt.xlim(left = 0)
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi tamponi", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Nuovi tamponi al giorno in {}".format(regione), size = 15)
        plt.legend()
        plt.grid()
        fig.savefig("pics/tamponi/tamponi_{}.png".format(regione), dpi = 100)
        plt.close(fig)