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
    plt.plot(date, raggruppati['dimessi_guariti'], color = "#006600", alpha = 0.8, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#006600', alpha=0.3)
    l1 = plt.scatter(x = max(date), y = raggruppati['dimessi_guariti'].tail(1), color = "#006600", alpha = 1)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Guariti", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Guariti - Italia", size = 15)
    plt.grid(alpha = 0.5)
    lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['dimessi_guariti'].tail(1).values[0]), 
    date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([raggruppati['dimessi_guariti'].tail(2).values[0], raggruppati['dimessi_guariti'].tail(3).values[0],
    raggruppati['dimessi_guariti'].tail(4).values[0],raggruppati['dimessi_guariti'].tail(5).values[0],raggruppati['dimessi_guariti'].tail(6).values[0],
    raggruppati['dimessi_guariti'].tail(7).values[0],raggruppati['dimessi_guariti'].tail(8).values[0],raggruppati['dimessi_guariti'].tail(9).values[0]])))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    fig.savefig("pics/guariti/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo
    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['dimessi_guariti']
        per_regioni = per_regioni.diff()
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni, color = "#006600", alpha = 0.8, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#006600', alpha=0.3)
        plt.scatter(x = max(date), y = per_regioni.tail(1), color = "#006600", alpha = 1,
        label = "{}: {}".format(date[-1].strftime("%d-%h"),int(per_regioni.tail(1).values[0])))
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Guariti", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Guariti - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), int(per_regioni.tail(1).values[0]), 
        date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([per_regioni.tail(2).values[0], per_regioni.tail(3).values[0],
        per_regioni.tail(4).values[0],per_regioni.tail(5).values[0],per_regioni.tail(6).values[0],
        per_regioni.tail(7).values[0],per_regioni.tail(8).values[0],per_regioni.tail(9).values[0]])))], 
        bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/guariti/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)

    fig, ax = plt.subplots()
    plt.plot(date[-30:], raggruppati['dimessi_guariti'][-30:], color = "#006600", alpha = 0.8, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#006600', alpha=0.3)
    l1 = plt.scatter(x = max(date), y = raggruppati['dimessi_guariti'].tail(1), color = "#006600", alpha = 1)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Guariti", size = 12)
    plt.xticks(size = 10, rotation = 0)
    plt.yticks(size = 10)
    plt.title("Guariti - Italia", size = 15)
    plt.grid(alpha = 0.5)
    lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['dimessi_guariti'].tail(1).values[0]), 
    date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([raggruppati['dimessi_guariti'].tail(2).values[0], raggruppati['dimessi_guariti'].tail(3).values[0],
    raggruppati['dimessi_guariti'].tail(4).values[0],raggruppati['dimessi_guariti'].tail(5).values[0],raggruppati['dimessi_guariti'].tail(6).values[0],
    raggruppati['dimessi_guariti'].tail(7).values[0],raggruppati['dimessi_guariti'].tail(8).values[0],raggruppati['dimessi_guariti'].tail(9).values[0]])))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    fig.savefig("pics/guariti_news/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo
    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['dimessi_guariti']
        per_regioni = per_regioni.diff()
        fig, ax = plt.subplots()
        plt.plot(date[-30:], per_regioni[-30:], color = "#006600", alpha = 0.8, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#006600', alpha=0.3)
        l1 = plt.scatter(x = max(date), y = per_regioni.tail(1), color = "#006600", alpha = 1)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Guariti", size = 12)
        plt.xticks(size = 10, rotation = 0)
        plt.yticks(size = 10)
        plt.title("Guariti - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), int(per_regioni.tail(1).values[0]), 
        date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([per_regioni.tail(2).values[0], per_regioni.tail(3).values[0],
        per_regioni.tail(4).values[0],per_regioni.tail(5).values[0],per_regioni.tail(6).values[0],
        per_regioni.tail(7).values[0],per_regioni.tail(8).values[0],per_regioni.tail(9).values[0]])))], 
        bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/guariti_news/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)