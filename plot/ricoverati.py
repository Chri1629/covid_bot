import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt



def ricoverati():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 

    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['ricoverati_con_sintomi'], color = "#0047c3", alpha = 0.8, linewidth =2)
    l1 = plt.scatter(x = date[-1], y = raggruppati['ricoverati_con_sintomi'].tail(1), color = "#0047c3", alpha = 1)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Ricoverati", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Ricoverati - Italia")
    lg = plt.legend([l1], ["{}: {}\n{}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['ricoverati_con_sintomi'].tail(1).values[0]), 
    date[-2].strftime("%d-%h"), int(raggruppati['ricoverati_con_sintomi'].tail(2).values[0]))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/ricoverati/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['ricoverati_con_sintomi']
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni, color = "#0047c3", alpha = 0.8, linewidth =2)
        l1 = plt.scatter(x = date[-1], y = per_regioni.tail(1), color = "#0047c3", alpha = 1,
        label = "{}: {}".format(date[-2].strftime("%d-%h"),int(per_regioni.tail(1).values[0])))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Ricoverati", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Ricoverati - {}".format(regione), size = 15)
        lg = plt.legend([l1], ["{}: {}\n{}: {}".format(date[-1].strftime("%d-%h"), int(per_regioni.tail(1).values[0]), 
        date[-2].strftime("%d-%h"), int(per_regioni.tail(2).values[0]))], 
        bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        plt.grid(alpha = 0.5)
        fig.savefig("pics/ricoverati/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)


    fig, ax = plt.subplots()
    plt.plot(date[-30:], raggruppati['ricoverati_con_sintomi'][-30:], color = "#0047c3", alpha = 0.8, linewidth =2)
    l1 = plt.scatter(x = date[-1], y = raggruppati['ricoverati_con_sintomi'].tail(1), color = "#0047c3", alpha = 1)

    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Ricoverati", size = 12)
    plt.xticks(size = 10, rotation=0)
    plt.yticks(size = 10)
    plt.title("Ricoverati - Italia")
    lg = plt.legend([l1], ["{}: {}\n{}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['ricoverati_con_sintomi'].tail(1).values[0]), 
    date[-2].strftime("%d-%h"), int(raggruppati['ricoverati_con_sintomi'].tail(2).values[0]))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/ricoverati_news/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['ricoverati_con_sintomi']
        fig, ax = plt.subplots()
        plt.plot(date[-30:], per_regioni[-30:], color = "#0047c3", alpha = 0.8, linewidth =2)
        l1 = plt.scatter(x = date[-1], y = per_regioni.tail(1), color = "#0047c3", alpha = 1)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Ricoverati", size = 12)
        plt.xticks(size = 10, rotation=0)
        plt.yticks(size = 10)
        plt.title("Ricoverati - {}".format(regione), size = 15)
        lg = plt.legend([l1], ["{}: {}\n{}: {}".format(date[-1].strftime("%d-%h"), int(per_regioni.tail(1).values[0]), 
        date[-2].strftime("%d-%h"), int(per_regioni.tail(2).values[0]))], 
        bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        plt.grid(alpha = 0.5)
        fig.savefig("pics/ricoverati_news/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)
    
    
    