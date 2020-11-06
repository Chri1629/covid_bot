import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt



def tamponi():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 

    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['tamponi'].diff(), color = "#e5e500", alpha = 0.8, linewidth =2)
    plt.scatter(x = max(date), y = raggruppati['tamponi'].diff().tail(1), color = "#e5e500", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(raggruppati['tamponi'].diff().tail(1).values[0])))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Nuovi tamponi", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Tamponi - Italia", size = 15)
    lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/tamponi/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['tamponi']
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni.diff(), color = "#e5e500", alpha = 0.8, linewidth =2)
        plt.scatter(x = max(date), y = per_regioni.diff().tail(1), color = "#e5e500", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(per_regioni.diff().tail(1).values[0])))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi tamponi", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Tamponi - {}".format(regione), size = 15)
        lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        plt.grid(alpha = 0.5)
        fig.savefig("pics/tamponi/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)
    
    fig, ax = plt.subplots()
    plt.plot(date[-14:], raggruppati['tamponi'].diff()[-14:], color = "#e5e500", alpha = 0.8, linewidth =2)
    plt.scatter(x = max(date), y = raggruppati['tamponi'].diff().tail(1), color = "#e5e500", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(raggruppati['tamponi'].diff().tail(1).values[0])))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Nuovi tamponi", size = 12)
    plt.xticks(size = 10, rotation = 35)
    plt.yticks(size = 10)
    plt.title("Tamponi - Italia", size = 15)
    lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/tamponi_news/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['tamponi']
        fig, ax = plt.subplots()
        plt.plot(date[-14:], per_regioni.diff()[-14:], color = "#e5e500", alpha = 0.8, linewidth =2)
        plt.scatter(x = max(date), y = per_regioni.diff().tail(1), color = "#e5e500", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(per_regioni.diff().tail(1).values[0])))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi tamponi", size = 12)
        plt.xticks(size = 10, rotation = 35)
        plt.yticks(size = 10)
        plt.title("Tamponi - {}".format(regione), size = 15)
        lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        plt.grid(alpha = 0.5)
        fig.savefig("pics/tamponi_news/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)
    
    
