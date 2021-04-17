import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

def vaccini_categorie():
   df = pd.read_csv("data/vaccini.csv", sep = ',')
   cols = ['categoria_operatori_sanitari_sociosanitari',
          'categoria_personale_non_sanitario', 'categoria_ospiti_rsa',
          'categoria_over80', 'categoria_forze_armate',
          'categoria_personale_scolastico', 'categoria_altro']
   df = df[cols]
   df = df.rename(columns = {'categoria_operatori_sanitari_sociosanitari' : 'Operatori Socio-Sanitari',
                        'categoria_personale_non_sanitario' : 'Personale NON sanitario', 
                        'categoria_ospiti_rsa' : 'Ospiti RSA',
                        'categoria_over80' : 'Over 80', 
                        'categoria_forze_armate' : 'Forze armate',
                        'categoria_personale_scolastico' : 'Personale Scolastico', 
                        'categoria_altro' : 'Altro'})
   # calcolo totale dosi simministrate per ciascuna categoria (somma)
   df_sum = df.sum()
   
   # plot
   fig, ax = plt.subplots()
   plt.barh(df_sum.index, df_sum.values, color = ['#54C575', '#00B798', '#00A4B4', '#008EC2', '#008DD0', '#0075BB', '#4D59A0'])
   
   plt.title("Somministrazioni per categoria di soggetti", fontdict = {'size': 15})
   plt.xlabel("num somministrazini", fontdict={'size':12})
   #plt.ticklabel_format(axis = 'x', style='plain')
   xticks = mtick.FuncFormatter(lambda x, p: format(int(x), ','))
   ax.xaxis.set_major_formatter(xticks)
   
   plt.grid(axis = 'x', linestyle = '--', alpha = 0.4)
   plt.savefig("pics/vaccini/categorie.png", dpi = 100, bbox_inches='tight')
   plt.close(fig)


def vaccini_fasce():
   df = pd.read_csv("data/vaccini.csv", sep = ',')
   
   df_fasce = df.groupby(['fascia_anagrafica']).sum()[['prima_dose', 'seconda_dose']]
   df_fasce['massimi'] = [2298846,6084382,6854632,8937229,9414195,7364364,5968373,3628160,791543] # massimi hardcoded
   
   fig, ax = plt.subplots(figsize=(6,7))
   
   ax.bar(df_fasce.index, df_fasce['prima_dose'], label='prima dose', color = 'forestgreen')
   ax.bar(df_fasce.index, df_fasce['seconda_dose'], label='seconda dose', color = 'gray')
   plt.scatter(df_fasce.index, df_fasce['massimi'], color = 'black', marker = 'v', label = 'traguardo')
   
   plt.title('Popolazione vaccinata per fasce d\'eta\'')
   plt.ylabel('Pop. vaccinata')
   yticks = mtick.FuncFormatter(lambda x, p: f'{round(x/1e+6)} mln')
   ax.yaxis.set_major_formatter(yticks)
   plt.legend()
   plt.grid(axis = 'y', linestyle='--', alpha = 0.4)
   fig.savefig("pics/vaccini/fasce.png", dpi = 100, bbox_inches='tight')
   plt.close(fig)
   
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
    l2 = plt.scatter(x = date[-1], y = raggruppati['seconda_dose'].tail(1), color = "gray", alpha = 1)

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
    
    #fmt = '%.0nf%' # Format you want the ticks, e.g. '40%'
    yticks = mtick.FuncFormatter(lambda x, p: format(int(x), ','))
    ax.yaxis.set_major_formatter(yticks)
    
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Somministazioni vaccini - Italia", size = 15)
    lg = plt.legend([l1, l2], ["Prima dose: {}".format(round(raggruppati['prima_dose'].tail(1).values[0],2)), 
                              "Seconda dose: {}".format(round(raggruppati['seconda_dose'].tail(1).values[0],2))])
    
    plt.grid(alpha = 0.5)
    fig.savefig("pics/vaccini/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)
    
def vaccini_cum():
    base = dt.datetime(2020, 12, 27)
    pop_ita = 59641488 # fonte istat
    dati_regione = pd.read_csv("data/vaccini_fixed.csv", sep = ",")
    raggruppati = dati_regione.groupby('data').sum().reset_index()
    date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 
    # somme cumulate
    raggruppati['prima_dose'] = (raggruppati['prima_dose'].cumsum()/pop_ita) * 100
    raggruppati['seconda_dose'] = (raggruppati['seconda_dose'].cumsum()/pop_ita) * 100
    
    fig, ax = plt.subplots()

    plt.plot(date, raggruppati['prima_dose'], color='forestgreen')
    plt.plot(date, raggruppati['seconda_dose'], color='gray')

    l1 = plt.scatter(x = date[-1], y = raggruppati['prima_dose'].tail(1), color = "forestgreen", alpha = 1)
    l2 = plt.scatter(x = date[-1], y = raggruppati['seconda_dose'].tail(1), color = "gray", alpha = 1)

    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    y1 = ax.lines[-2].get_ydata()

    ax.fill_between(x, y, y1, color='forestgreen', alpha=0.3)
    ax.fill_between(x, 0, y, color='gray', alpha=0.3)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Pop. vaccinata", size = 12)
    
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)
    plt.xticks(size = 10)
    
    plt.yticks(size = 10)
    plt.title("Percentuale vaccini - Italia", size = 15)
    lg = plt.legend([l1, l2], ["Prima dose: {}%".format(round(raggruppati['prima_dose'].tail(1).values[0],2)), 
                              "Seconda dose: {}%".format(round(raggruppati['seconda_dose'].tail(1).values[0],2))])
    plt.grid(alpha = 0.5)
    fig.savefig("pics/vaccini/italia_cum.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)
  