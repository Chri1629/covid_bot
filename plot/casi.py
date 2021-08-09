import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates

def casi():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    raggruppati['pos_ma'] = raggruppati[['data', 'nuovi_positivi']].rolling(window = 7).mean() # week moving average
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 
    
    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['nuovi_positivi'], color = "#c90000", alpha = 0.5, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#c90000', alpha=0.2)
    plt.plot(date, raggruppati['pos_ma'], color = "#c90000", alpha = 1, linewidth =2)
    l1 = plt.scatter(x = max(date), y = raggruppati['nuovi_positivi'].tail(1).values[0], color = "#c90000", alpha = 1)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Nuovi casi", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Nuovi casi - Italia", size = 15)
    lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), raggruppati['nuovi_positivi'].tail(1).values[0], 
    date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([raggruppati['nuovi_positivi'].tail(2).values[0], raggruppati['nuovi_positivi'].tail(3).values[0],
    raggruppati['nuovi_positivi'].tail(4).values[0],raggruppati['nuovi_positivi'].tail(5).values[0],raggruppati['nuovi_positivi'].tail(6).values[0],
    raggruppati['nuovi_positivi'].tail(7).values[0],raggruppati['nuovi_positivi'].tail(8).values[0],raggruppati['nuovi_positivi'].tail(9).values[0]])))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/nuovi_positivi/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['nuovi_positivi']
        pos_ma_regioni = per_regioni.rolling(window = 7).mean() # week moving average
        
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni, color = "#c90000", alpha = 0.5, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#c90000', alpha=0.2)
        plt.plot(date, pos_ma_regioni, color = "#c90000", alpha = 1, linewidth =2)
        l1 = plt.scatter(x = max(date), y = per_regioni.tail(1), color = "#c90000", alpha = 1)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi casi", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Nuovi casi - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), per_regioni.tail(1).values[0], 
        date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([per_regioni.tail(2).values[0], per_regioni.tail(3).values[0],
        per_regioni.tail(4).values[0],per_regioni.tail(5).values[0],per_regioni.tail(6).values[0],
        per_regioni.tail(7).values[0],per_regioni.tail(8).values[0],per_regioni.tail(9).values[0]])))], 
        bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/nuovi_positivi/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)

    
    fig, ax = plt.subplots()
    plt.plot(date[-30:], raggruppati['nuovi_positivi'][-30:], color = "#c90000", alpha = 0.5, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#c90000', alpha=0.2)
    plt.plot(date[-30:], raggruppati['pos_ma'][-30:], color = "#c90000", alpha = 1, linewidth =2)
    l1 = plt.scatter(x = max(date), y = raggruppati['nuovi_positivi'].tail(1).values[0], color = "#c90000", alpha = 1)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Nuovi casi", size = 12)
    plt.xticks(size = 10, rotation = 0)
    plt.yticks(size = 10)
    plt.title("Nuovi casi - Italia", size = 15)
    lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), raggruppati['nuovi_positivi'].tail(1).values[0], 
    date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([raggruppati['nuovi_positivi'].tail(2).values[0], raggruppati['nuovi_positivi'].tail(3).values[0],
    raggruppati['nuovi_positivi'].tail(4).values[0],raggruppati['nuovi_positivi'].tail(5).values[0],raggruppati['nuovi_positivi'].tail(6).values[0],
    raggruppati['nuovi_positivi'].tail(7).values[0],raggruppati['nuovi_positivi'].tail(8).values[0],raggruppati['nuovi_positivi'].tail(9).values[0]])))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/nuovi_positivi_news/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['nuovi_positivi']
        pos_ma_regioni = per_regioni.rolling(window = 7).mean() # week moving average
        
        fig, ax = plt.subplots()
        plt.plot(date[-30:], per_regioni[-30:], color = "#c90000", alpha = 0.5, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#c90000', alpha=0.2)
        plt.plot(date[-30:], pos_ma_regioni[-30:], color = "#c90000", alpha = 1, linewidth =2)
        l1 = plt.scatter(x = max(date), y = per_regioni.tail(1), color = "#c90000", alpha = 1)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi casi", size = 12)
        plt.xticks(size = 10, rotation = 0)
        plt.yticks(size = 10)
        plt.title("Nuovi casi - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), per_regioni.tail(1).values[0], 
        date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([per_regioni.tail(2).values[0], per_regioni.tail(3).values[0],
        per_regioni.tail(4).values[0],per_regioni.tail(5).values[0],per_regioni.tail(6).values[0],
        per_regioni.tail(7).values[0],per_regioni.tail(8).values[0],per_regioni.tail(9).values[0]])))], 
        bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/nuovi_positivi_news/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)