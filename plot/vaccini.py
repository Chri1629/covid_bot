import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import datetime as dt



def vaccini():
    base = dt.datetime(2020, 12, 27)
    dati_regione = pd.read_csv("data/vaccini_fixed.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 

    fig, ax = plt.subplots()

    plt.plot(date, raggruppati['prima_dose']+raggruppati['seconda_dose'], color='forestgreen')
    plt.plot(date, raggruppati['seconda_dose'], color='gray')

    l1 = plt.scatter(x = date[-1], y = raggruppati['prima_dose'].tail(1) + raggruppati['seconda_dose'].tail(1), color = "forestgreen", alpha = 1)

    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    y1 = ax.lines[-2].get_ydata()

    ax.fill_between(x, y, y1, color='forestgreen', alpha=0.3)
    ax.fill_between(x, 0, y, color='gray', alpha=0.3)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Vaccini", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Vaccini - Italia")
    lg = plt.legend([l1], ["Tot {}: {}\nTot {}: {}".format(date[-1].strftime("%d-%h"), int(raggruppati['prima_dose'].tail(1).values[0] + raggruppati['seconda_dose'].tail(1).values[0]), 
    date[-2].strftime("%d-%h"), int(raggruppati['prima_dose'].tail(2).values[0] + raggruppati['seconda_dose'].tail(2).values[0]))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/vaccini/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)
  