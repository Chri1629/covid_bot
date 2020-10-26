import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def ricoverati():
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))

    fig = plt.figure(figsize = (6,4))
    plt.plot(date, raggruppati['ricoverati_con_sintomi'], color = "skyblue", alpha = 1)
    plt.scatter(x = max(date), y = raggruppati['ricoverati_con_sintomi'].tail(1), 
        label = "Ultimo valore: {}".format(int(raggruppati['ricoverati_con_sintomi'].tail(1).values[0])))

    plt.xlim(left = 0)
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Terapia intensiva", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Attualmente ricoverati in Italia")
    plt.legend()
    plt.grid()
    fig.savefig("pics/ricoverati/ricoverati.png", dpi = 100)
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['ricoverati_con_sintomi']
        fig = plt.figure(figsize = (6,4))
        plt.plot(date, per_regioni, color = "skyblue", alpha = 1)
        plt.scatter(x = max(date), y = per_regioni.tail(1), label = "Ultimo valore: {}".format(int(per_regioni.tail(1).values[0])))
        plt.xlim(left = 0)
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Ricoverati", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Attualmente ricoverati in {}".format(regione), size = 15)
        plt.legend()
        plt.grid()
        fig.savefig("pics/ricoverati/ricoverati_{}.png".format(regione.lower()), dpi = 100)
        plt.close(fig)
    