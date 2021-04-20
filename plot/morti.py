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
    plt.plot(date, raggruppati['deceduti'].diff(), color = "#464646", alpha = 0.8, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#464646', alpha=0.3)
    l1 = plt.scatter(x = date[-1], y = raggruppati['deceduti'].diff().tail(1), color = "#464646", alpha = 1)
    plt.hlines(y = raggruppati['deceduti'].diff().max(), xmin=base, xmax=date[-1], linestyles="--")
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Morti", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Deceduti - Italia", size = 15)
    lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['deceduti'].diff().tail(1).values[0]), 
    date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([raggruppati['deceduti'].diff().tail(2).values[0], raggruppati['deceduti'].diff().tail(3).values[0],
    raggruppati['deceduti'].diff().tail(4).values[0],raggruppati['deceduti'].diff().tail(5).values[0],raggruppati['deceduti'].diff().tail(6).values[0],
    raggruppati['deceduti'].diff().tail(7).values[0],raggruppati['deceduti'].diff().tail(8).values[0],raggruppati['deceduti'].diff().tail(9).values[0]])))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    plt.savefig("pics/morti/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['deceduti']
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni.diff(), color = "#464646", alpha = 0.8, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#464646', alpha=0.3)
        l1 = plt.scatter(x = date[-1], y = per_regioni.diff().tail(1), color = "#464646", alpha = 1)
        plt.hlines(y = per_regioni.diff().max(), xmin=base,xmax=date[-1], linestyles="--")
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi morti", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Deceduti - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), int(per_regioni.diff().tail(1).values[0]), 
        date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([per_regioni.diff().tail(2).values[0], per_regioni.diff().tail(3).values[0],
        per_regioni.diff().tail(4).values[0],per_regioni.diff().tail(5).values[0],per_regioni.diff().tail(6).values[0],
        per_regioni.diff().tail(7).values[0],per_regioni.diff().tail(8).values[0],per_regioni.diff().tail(9).values[0]])))], 
        bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/morti/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)

    fig, ax = plt.subplots()
    plt.plot(date[-30:], raggruppati['deceduti'].diff()[-30:], color = "#464646", alpha = 0.8, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#464646', alpha=0.3)
    l1 = plt.scatter(x = date[-1], y = raggruppati['deceduti'].diff().tail(1), color = "#464646", alpha = 1)
    plt.hlines(y = raggruppati['deceduti'].diff().max(), xmin=date[-30], xmax=date[-1], linestyles="--")
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Morti", size = 12)
    plt.xticks(size = 10, rotation=0)
    plt.yticks(size = 10)
    plt.title("Deceduti - Italia", size = 15)
    lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['deceduti'].diff().tail(1).values[0]), 
    date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([raggruppati['deceduti'].diff().tail(2).values[0], raggruppati['deceduti'].diff().tail(3).values[0],
    raggruppati['deceduti'].diff().tail(4).values[0],raggruppati['deceduti'].diff().tail(5).values[0],raggruppati['deceduti'].diff().tail(6).values[0],
    raggruppati['deceduti'].diff().tail(7).values[0],raggruppati['deceduti'].diff().tail(8).values[0],raggruppati['deceduti'].diff().tail(9).values[0]])))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    plt.savefig("pics/morti_news/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['deceduti']
        fig, ax = plt.subplots()
        plt.plot(date[-30:], per_regioni.diff()[-30:], color = "#464646", alpha = 0.8, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#464646', alpha=0.3)
        l1 = plt.scatter(x = date[-1], y = per_regioni.diff().tail(1), color = "#464646", alpha = 1)
        plt.hlines(y = per_regioni.diff().max(), xmin=date[-30],xmax=date[-1], linestyles="--")
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi morti", size = 12)
        plt.xticks(size = 10, rotation=0)
        plt.yticks(size = 10)
        plt.title("Deceduti - {}".format(regione), size = 15)
        plt.grid(alpha = 0.5)
        lg = plt.legend([l1], ["{}: {}\n{}-{}: {}".format(date[-1].strftime("%d-%h"), int(per_regioni.diff().tail(1).values[0]), 
        date[-9].strftime("%d-%h"), date[-2].strftime("%d-%h"), int(np.mean([per_regioni.diff().tail(2).values[0], per_regioni.diff().tail(3).values[0],
        per_regioni.diff().tail(4).values[0],per_regioni.diff().tail(5).values[0],per_regioni.diff().tail(6).values[0],
        per_regioni.diff().tail(7).values[0],per_regioni.diff().tail(8).values[0],per_regioni.diff().tail(9).values[0]])))], 
        bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
        fig.savefig("pics/morti_news/{}.png".format(regione.lower()), dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
        plt.close(fig)