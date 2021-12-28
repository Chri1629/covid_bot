import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates

def att_positivi():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 
    
    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['totale_positivi'], color = "#8A2BE2", alpha = 0.8, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#8A2BE2', alpha=0.2)
    #plt.plot(date, raggruppati['pos_ma'], color = "#c90000", alpha = 1, linewidth =2)
    l1 = plt.scatter(x = max(date), y = raggruppati['totale_positivi'].tail(1).values[0], color = "#8A2BE2", alpha = 1)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Attuali positivi", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Attuali positivi - Italia", size = 15)
    plt.legend([l1], ["{}: {}".format(date[-1].strftime("%d-%h"), raggruppati['totale_positivi'].tail(1).values[0])], bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/att_positivi/italia.png", dpi = 100, bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['totale_positivi']
        
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni, color = "#8A2BE2", alpha = 0.7, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#8A2BE2', alpha=0.2)
        l1 = plt.scatter(x = max(date), y = per_regioni.tail(1), color = "#8A2BE2", alpha = 1)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Attuali positivi", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Attuali positivi - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        plt.legend([l1], ["{}: {}".format(date[-1].strftime("%d-%h"), per_regioni.tail(1).values[0])], bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/att_positivi/{}.png".format(regione.lower()), dpi = 100, bbox_inches='tight')
        plt.close(fig)

    
    fig, ax = plt.subplots()
    plt.plot(date[-30:], raggruppati['totale_positivi'][-30:], color = "#8A2BE2", alpha = 0.7, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#8A2BE2', alpha=0.2)
    l1 = plt.scatter(x = max(date), y = raggruppati['totale_positivi'].tail(1).values[0], color = "#8A2BE2", alpha = 1)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Attuali positivi", size = 12)
    plt.xticks(size = 10, rotation = 0)
    plt.yticks(size = 10)
    plt.title("Attuali positivi - Italia", size = 15)
    plt.legend([l1], ["{}: {}".format(date[-1].strftime("%d-%h"), raggruppati['totale_positivi'].tail(1).values[0])], bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/att_positivi_news/italia.png", dpi = 100, bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['totale_positivi']
        
        fig, ax = plt.subplots()
        plt.plot(date[-30:], per_regioni[-30:], color = "#8A2BE2", alpha = 0.7, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#8A2BE2', alpha=0.2)
        l1 = plt.scatter(x = max(date), y = per_regioni.tail(1), color = "#8A2BE2", alpha = 1)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Attuali positivi", size = 12)
        plt.xticks(size = 10, rotation = 0)
        plt.yticks(size = 10)
        plt.title("Attuali positivi - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        plt.legend([l1], ["{}: {}".format(date[-1].strftime("%d-%h"), per_regioni.tail(1).values[0])], bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/att_positivi_news/{}.png".format(regione.lower()), dpi = 100, bbox_inches='tight')
        plt.close(fig)