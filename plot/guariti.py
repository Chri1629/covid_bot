import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt



def guariti():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    raggruppati['dimessi_guariti'] = raggruppati['dimessi_guariti'].diff()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 

    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['dimessi_guariti'], color = "black", alpha = 0.7)
    plt.scatter(x = max(date), y = raggruppati['dimessi_guariti'].tail(1), color = "black",
    label = "Ultimo valore: {}".format(int(raggruppati['dimessi_guariti'].tail(1).values[0])))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Guariti", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Guariti in Italia", size = 15)
    plt.grid()
    plt.legend()
    fig.savefig("pics/guariti/italia.png", dpi = 100)
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo
    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['dimessi_guariti']
        per_regioni = per_regioni.diff()
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni, color = "black", alpha = 0.7)
        plt.scatter(x = max(date), y = per_regioni.tail(1), color = "black",
        label = "Ultimo valore: {}".format(int(per_regioni.tail(1).values[0])))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Guariti", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Guariti in {}".format(regione), size = 15)
        plt.grid()
        plt.legend()
        fig.savefig("pics/guariti/{}.png".format(regione.lower()), dpi = 100)
        plt.close(fig)