import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt

# y axis formatter
def millions(x, pos):
    """The two arguments are the value and tick position."""
    return '{:1.1f} mln'.format(x*1e-6)

def tamponi():
    base = dt.datetime(2020, 2, 24)
    dati_regione = pd.read_csv("data/dati_regioni.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    raggruppati['ma'] = raggruppati['tamponi'].rolling(window = 7).mean() # week moving average
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 

    fig, ax = plt.subplots()
    plt.plot(date, raggruppati['tamponi'].diff(), color = "#e5e500", alpha = 0.5, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#e5e500', alpha=0.2)
    plt.plot(date, raggruppati['ma'].diff(), color = "#e5e500", alpha = 1, linewidth =2, label = 'weekly avg.')
    lbl_scatter = "{}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['tamponi'].diff().tail(1).values[0]))
    plt.scatter(x = max(date), y = raggruppati['tamponi'].diff().tail(1), color = "#e5e500", alpha = 1, label = lbl_scatter)
    #ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.yaxis.set_major_formatter(millions)
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Nuovi tamponi", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Tamponi - Italia", size = 15)
    ax.legend()
    plt.grid(alpha = 0.5)
    fig.savefig("pics/tamponi/italia.png", dpi = 100, bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['tamponi']
        pos_ma_regioni = per_regioni.diff().rolling(window = 7).mean() # week moving average
        fig, ax = plt.subplots()
        plt.plot(date, per_regioni.diff(), color = "#e5e500", alpha = 0.5, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#e5e500', alpha=0.2)
        plt.plot(date, pos_ma_regioni, color = "#e5e500", alpha = 1, linewidth =2, label = 'weekly avg.')
        lbl_scatter = "{}: {}".format(date[-1].strftime("%d-%h"), int(per_regioni.diff().tail(1).values[0]))
        plt.scatter(x = max(date), y = per_regioni.diff().tail(1), color = "#e5e500", alpha = 1, label = lbl_scatter)
       # ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi tamponi", size = 12)
        plt.xticks(size = 10)
        plt.yticks(size = 10)
        plt.title("Tamponi - {}".format(regione), size = 15)
        ax.legend()
        plt.grid(alpha = 0.5)
        fig.savefig("pics/tamponi/{}.png".format(regione.lower()), dpi = 100, bbox_inches='tight')
        plt.close(fig)
    
    fig, ax = plt.subplots()
    plt.plot(date[-30:], raggruppati['tamponi'].diff()[-30:], color = "#e5e500", alpha = 0.5, linewidth =2)
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    ax.fill_between(x, 0, y, color='#e5e500', alpha=0.2)
    plt.plot(date[-30:], raggruppati['ma'].diff()[-30:], color = "#e5e500", alpha = 1, linewidth =2, label = 'weekly avg.')
    lbl_scatter = "{}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['tamponi'].diff().tail(1).values[0]))
    plt.scatter(x = max(date), y = raggruppati['tamponi'].diff().tail(1), color = "#e5e500", alpha = 1, label = lbl_scatter)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
    ax.yaxis.set_major_formatter(millions)
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Nuovi tamponi", size = 12)
    plt.xticks(size = 10, rotation = 0)
    plt.yticks(size = 10)
    plt.title("Tamponi - Italia", size = 15)
    ax.legend()
    plt.grid(alpha = 0.5)
    fig.savefig("pics/tamponi_news/italia.png", dpi = 100, bbox_inches='tight')
    plt.close(fig)

    ## Provo a raggruppare per regione e a stamprarli anche per regione quindi vanno messi dentro un for e bisogna fare un ciclo

    for regione in dati_regione['denominazione_regione'].unique():
        per_regioni = dati_regione.loc[dati_regione['denominazione_regione'] == regione]['tamponi']
        pos_ma_regioni = per_regioni.diff().rolling(window = 7).mean() # week moving average
        fig, ax = plt.subplots()
        plt.plot(date[-30:], per_regioni.diff()[-30:], color = "#e5e500", alpha = 0.5, linewidth =2)
        x = ax.lines[-1].get_xdata()
        y = ax.lines[-1].get_ydata()
        ax.fill_between(x, 0, y, color='#e5e500', alpha=0.2)
        plt.plot(date[-30:], pos_ma_regioni[-30:], color = "#e5e500", alpha = 1, linewidth =2, label = 'weekly avg.')
        lbl_scatter = "{}: {}".format(date[-1].strftime("%d-%h"), int(per_regioni.diff().tail(1).values[0]))
        plt.scatter(x = max(date), y = per_regioni.diff().tail(1), color = "#e5e500", alpha = 1, label = lbl_scatter)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = 4))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%h'))
        plt.ylim(bottom = 0)
        plt.xlabel("Data", size = 12)
        plt.ylabel("Nuovi tamponi", size = 12)
        plt.xticks(size = 10, rotation = 0)
        plt.yticks(size = 10)
        plt.title("Tamponi - {}".format(regione), size = 15)
        ax.legend()
        plt.grid(alpha = 0.5)
        fig.savefig("pics/tamponi_news/{}.png".format(regione.lower()), dpi = 100, bbox_inches='tight')
        plt.close(fig)
    
    
