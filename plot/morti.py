import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates



def morti():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 

    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['deceduti'].diff(), color = "red", alpha = 0.4)
    plt.scatter(x = date[-1], y = raggruppati['deceduti'].diff().tail(1), color = "red", 
        label = "Ultimo valore {}".format(int(raggruppati['deceduti'].diff().tail(1).values[0])))
    plt.hlines(y = raggruppati['deceduti'].diff().max(), xmin=base, xmax=date[-1], label="Picco massimo")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Morti", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Deceduti per giorno in Italia", size = 15)
    plt.legend()
    plt.grid()
    plt.savefig("pics/morti/italia.png", dpi = 100)
    plt.close(fig)

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['deceduti']
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni.diff(), color = "red", alpha = 0.4)
        plt.scatter(x = date[-1], y = per_regioni.diff().tail(1), color = "red",
        label = "Ultimo valore {}".format(int(per_regioni.diff().tail(1).values[0])))
        plt.hlines(y = per_regioni.diff().max(), xmin=base,xmax=date[-1], label="Picco massimo")
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi morti", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Deceduti al giorno in {}".format(regione), size = 15)
        plt.grid()
        plt.legend()
        fig.savefig("pics/morti/{}.png".format(regione.lower()), dpi = 100)
        plt.close(fig)