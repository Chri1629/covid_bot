import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt



def terapia_intensiva():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 
    posti_letto = pd.read_csv("data/regioni.csv", sep = ",") 
    posti_letto_totali = posti_letto['posti_letto'].sum()

    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['terapia_intensiva'], color = "#00a9c3", alpha = 0.8, linewidth =2)
    plt.scatter(x = date[-1], y = raggruppati['terapia_intensiva'].tail(1), color = "#00a9c3", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(raggruppati['terapia_intensiva'].tail(1).values[0])))

    plt.hlines(y = posti_letto_totali, xmin = date[1], xmax=date[-1], color = "black", alpha = 0.7, linestyles = "--",
        label = "Posti disponibili: {}".format(posti_letto_totali))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Terapia intensiva", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Attualmente in terapia intensiva in Italia\n{}% occupati".format(round(raggruppati['terapia_intensiva'].tail(1).values[0]/posti_letto_totali*100),2), 
    size = 15)
    lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/terapia/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['terapia_intensiva']
        numero_posti_letto = posti_letto.loc[posti_letto['regione'] ==  regione]['posti_letto']
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni, color = "#00a9c3", alpha = 0.8, linewidth =2)
        plt.scatter(x = date[-1], y = per_regioni.tail(1), color = "#00a9c3", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(per_regioni.tail(1).values[0])))
        plt.hlines(y = numero_posti_letto, xmin = date[1], xmax=date[-1], color="black", alpha = 0.7, linestyles = "--",
        label = "Posti disponibili: {}".format(numero_posti_letto.values[0]))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Terapia intensiva", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Attualmente in terapia intensiva in {}\n{}% occupati".format(regione,
        round(per_regioni.tail(1).values[0]/numero_posti_letto.values[0]*100,2)), size = 15)
        lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        plt.grid(alpha = 0.5)
        fig.savefig("pics/terapia/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)

    fig, ax = plt.subplots()
    plt.plot(date[-14:], raggruppati['terapia_intensiva'][-14:], color = "#00a9c3", alpha = 0.8, linewidth =2)
    plt.scatter(x = date[-1], y = raggruppati['terapia_intensiva'].tail(1), color = "#00a9c3", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(raggruppati['terapia_intensiva'].tail(1).values[0])))

    plt.hlines(y = posti_letto_totali, xmin = date[-14], xmax=date[-1], color = "black", alpha = 0.7, linestyles = "--",
        label = "Posti disponibili: {}".format(posti_letto_totali))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Terapia intensiva", size = 12)
    plt.xticks(size = 10, rotation=35)
    plt.yticks(size = 10)
    plt.title("Attualmente in terapia intensiva in Italia\n{}% occupati".format(round(raggruppati['terapia_intensiva'].tail(1).values[0]/posti_letto_totali*100),2), 
    size = 15)
    lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/terapia_news/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['terapia_intensiva']
        numero_posti_letto = posti_letto.loc[posti_letto['regione'] ==  regione]['posti_letto']
        fig, ax = plt.subplots()
        plt.plot(date[-14:], per_regioni[-14:], color = "#00a9c3", alpha = 0.8, linewidth =2)
        plt.scatter(x = date[-1], y = per_regioni.tail(1), color = "#00a9c3", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(per_regioni.tail(1).values[0])))
        plt.hlines(y = numero_posti_letto, xmin = date[-14], xmax=date[-1], color="black", alpha = 0.7, linestyles = "--",
        label = "Posti disponibili: {}".format(numero_posti_letto.values[0]))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Terapia intensiva", size = 12)
        plt.xticks(size = 10, rotation=35)
        plt.yticks(size = 10)
        plt.title("Attualmente in terapia intensiva in {}\n{}% occupati".format(regione,
        round(per_regioni.tail(1).values[0]/numero_posti_letto.values[0]*100,2)), size = 15)
        lg = plt.legend(bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        plt.grid(alpha = 0.5)
        fig.savefig("pics/terapia_news/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)
    