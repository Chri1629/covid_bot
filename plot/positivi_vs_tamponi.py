import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt



def positivi_tamponi():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    raggruppati['tamponi'] = raggruppati['tamponi'].diff()
    raggruppati['rapporto_totale'] = round(raggruppati['nuovi_positivi']/raggruppati['tamponi']*100,2)
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 

    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['rapporto_totale'], color = "#da7400", alpha = 0.8, linewidth =2)
    plt.scatter(x = max(date), y = raggruppati['rapporto_totale'].tail(1), color = "#da7400", alpha = 1,
    label = "{}: {}%".format(date[-1].strftime("%d-%h"), raggruppati['rapporto_totale'].tail(1).values[0]))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Rapporto (%)", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("% Tamponi positivi - Italia", size = 15)
    plt.grid(alpha = 0.5)
    lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    fig.savefig("pics/rapporto_tamponi/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo
    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione][['nuovi_positivi','tamponi']]
        per_regioni['tamponi'] = per_regioni['tamponi'].diff()
        per_regioni['rapporto'] = round(per_regioni['nuovi_positivi']/per_regioni['tamponi']*100,1)
    
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni['rapporto'], color = "#da7400", alpha = 0.8, linewidth =2)
        plt.scatter(x = max(date), y = per_regioni['rapporto'].tail(1), color = "#da7400", alpha = 1,
        label = "{}: {}%".format(date[-1].strftime("%d-%h"),per_regioni['rapporto'].tail(1).values[0]))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Rapporto (%)", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("% Tamponi positivi - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/rapporto_tamponi/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)


    fig, ax = plt.subplots()
    plt.plot(date[-30:], raggruppati['rapporto_totale'][-30:], color = "#da7400", alpha = 0.8, linewidth =2)
    plt.scatter(x = max(date), y = raggruppati['rapporto_totale'].tail(1), color = "#da7400", alpha = 1,
    label = "{}: {}%".format(date[-1].strftime("%d-%h"), raggruppati['rapporto_totale'].tail(1).values[0]))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Rapporto (%)", size = 12)
    plt.xticks(size = 10, rotation=0)
    plt.yticks(size = 10)
    plt.title("% Tamponi positivi - Italia", size = 15)
    plt.grid(alpha = 0.5)
    lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    fig.savefig("pics/rapporto_tamponi_news/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo
    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione][['nuovi_positivi','tamponi']]
        per_regioni['tamponi'] = per_regioni['tamponi'].diff()
        per_regioni['rapporto'] = round(per_regioni['nuovi_positivi']/per_regioni['tamponi']*100,1)
    
        fig, ax = plt.subplots()
        plt.plot(date[-30:], per_regioni['rapporto'][-30:], color = "#da7400", alpha = 0.8, linewidth =2)
        plt.scatter(x = max(date), y = per_regioni['rapporto'].tail(1), color = "#da7400", alpha = 1,
        label = "{}: {}%".format(date[-1].strftime("%d-%h"),per_regioni['rapporto'].tail(1).values[0]))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Rapporto (%)", size = 12)
        plt.xticks(size = 10, rotation=0)
        plt.yticks(size = 10)
        plt.title("% Tamponi positivi - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/rapporto_tamponi_news/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)
        