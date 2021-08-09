import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
from matplotlib.patches import Rectangle

def vaccini_fasce():
   df = pd.read_csv("data/vaccini.csv", sep = ',')
   df_fasce = df.groupby(['fascia_anagrafica']).sum()[['prima_dose', 'seconda_dose']]
   df_fasce.loc['80+'] = df_fasce.loc['80-89'] + df_fasce.loc['90+']
   df_fasce.drop(['80-89', '90+'], inplace = True)
   
   df_platea = pd.read_csv("data/vaccini_platea.csv", sep = ',')

   df_fasce['massimi'] = df_platea.groupby('fascia_anagrafica').sum()['totale_popolazione'] # massima popolazione per fascia
   
   fig, ax = plt.subplots(figsize=(6,7))
   
   ax.bar(df_fasce.index, df_fasce['prima_dose'], label='prima dose', color = 'forestgreen')
   ax.bar(df_fasce.index, df_fasce['seconda_dose'], label='seconda dose', color = 'gray')
   plt.scatter(df_fasce.index, df_fasce['massimi'], color = 'black', marker = 'v', label = 'traguardo')
   
   plt.title('Popolazione vaccinata per fasce d\'eta\'')
   plt.ylabel('Popolazione vaccinata')
   yticks = mtick.FuncFormatter(lambda x, p: f'{round(x/1e+6)} mln')
   ax.yaxis.set_major_formatter(yticks)
   plt.legend()
   plt.grid(axis = 'y', linestyle='--', alpha = 0.4)
   fig.savefig("pics/vaccini/fasce.png", dpi = 100, bbox_inches='tight')
   plt.close(fig)

def vaccini_fasce_perc():
   df = pd.read_csv("data/vaccini.csv", sep = ',')
   df_fasce = df.groupby(['fascia_anagrafica']).sum()[['prima_dose', 'seconda_dose']]
   df_fasce.loc['80+'] = df_fasce.loc['80-89'] + df_fasce.loc['90+']
   df_fasce.drop(['80-89', '90+'], inplace = True)
   
   df_platea = pd.read_csv("data/vaccini_platea.csv", sep = ',')

   df_fasce['massimi'] = df_platea.groupby('fascia_anagrafica').sum()['totale_popolazione'] # massima popolazione per fascia
   perc_prima = df_fasce['prima_dose'].sum()/df_fasce['massimi'].sum()*100
   perc_seconda = df_fasce['seconda_dose'].sum()/df_fasce['massimi'].sum()*100
   
   df_fasce['prima_dose'] = df_fasce['prima_dose']/df_fasce['massimi']*100
   df_fasce['seconda_dose'] = df_fasce['seconda_dose']/df_fasce['massimi']*100
   
   fig, ax = plt.subplots(figsize=(6,7))
   
   ax.bar(df_fasce.index, df_fasce['prima_dose'], label=f'prima dose ({round(perc_prima, 2)}%)', color = 'forestgreen')
   ax.bar(df_fasce.index, df_fasce['seconda_dose'], label=f'seconda dose ({round(perc_seconda, 2)}%)', color = 'gray')
   #plt.scatter(df_fasce.index, 100, color = 'black', marker = 'v', label = 'traguardo')
   
   plt.title('Percentuale di popolazione vaccinata per fasce d\'eta\' - Italia')
   plt.ylabel('Percentuale pop. vaccinata')
   ax.yaxis.set_major_formatter(mtick.PercentFormatter())
   ax.yaxis.set_ticks(np.linspace(10, 100, 10))
   plt.legend()
   plt.grid(axis = 'y', linestyle='--', alpha = 0.7)
   fig.savefig("pics/vaccini/fasce_perc.png", dpi = 100, bbox_inches='tight')
   plt.close(fig)
   
def vaccini():
   base = dt.datetime(2020, 12, 27)
   dati_regione = pd.read_csv("data/vaccini_fixed.csv", sep = ",")
   raggruppati = dati_regione.groupby('data').sum().reset_index()
   raggruppati['prima_dose_ma'] = (raggruppati['prima_dose']+raggruppati['seconda_dose']).rolling(window = 7).mean()
   raggruppati['seconda_dose_ma'] = raggruppati['seconda_dose'].rolling(window = 7).mean()
   date = np.linspace(0,len(raggruppati['data'].unique()), len(raggruppati))
   date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 
   

   fig, ax = plt.subplots()

   plt.plot(date, raggruppati['prima_dose']+raggruppati['seconda_dose'], color='forestgreen', alpha = 0.8)
   plt.plot(date, raggruppati['seconda_dose'], color='gray', alpha = 0.8)

   l1 = plt.scatter(x = date[-1], y = raggruppati['prima_dose'].tail(1) + raggruppati['seconda_dose'].tail(1), color = "forestgreen", alpha = 1)
   l2 = plt.scatter(x = date[-1], y = raggruppati['seconda_dose'].tail(1), color = "gray", alpha = 1)
   l3 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)

   x = ax.lines[-1].get_xdata()
   y = ax.lines[-1].get_ydata()
   y1 = ax.lines[-2].get_ydata()

   ax.fill_between(x, y, y1, color='forestgreen', alpha=0.2)
   ax.fill_between(x, 0, y, color='gray', alpha=0.2)
   
   plt.plot(date, raggruppati['prima_dose_ma'], color = "forestgreen", alpha = 1, linewidth =2)
   plt.plot(date, raggruppati['seconda_dose_ma'], color = "gray", alpha = 1, linewidth =2)
   
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
   plt.title("Somministazioni giornaliere - Italia", size = 15)
   lg = plt.legend([l1, l2, l3], ["Prima dose: {}".format(round(raggruppati['prima_dose'].tail(1).values[0],2)), 
                           "Seconda dose: {}".format(round(raggruppati['seconda_dose'].tail(1).values[0],2)),
                           "Tot. somministrazioni: {} mln".format(round((raggruppati['prima_dose'].sum() + raggruppati['seconda_dose'].sum())/1e+06,3))])
   
   plt.grid(alpha = 0.5)
   fig.savefig("pics/vaccini/italia.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
   plt.close(fig)
    
def vaccini_cum():
   base = dt.datetime(2020, 12, 27)
   df_platea = pd.read_csv("data/vaccini_platea.csv", sep = ',')
   pop_ita = df_platea.sum()['totale_popolazione'] # fonte istat
   
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
   plt.ylabel("Popolazione vaccinata", size = 12)
   
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



# PLOT REGIONI
def vaccini_reg():
   base = dt.datetime(2020, 12, 27)
   dati_regione = pd.read_csv("data/vaccini_reg.csv", sep = ",")
   dati_regione['nome_area'].replace('Provincia Autonoma Trento', 'p.a. Trento', inplace = True)
   dati_regione['nome_area'].replace('Provincia Autonoma Bolzano / Bozen', 'p.a. Bolzano', inplace = True)
   dati_regione['nome_area'].replace("Valle d'Aosta / Vallée d'Aoste", "Valle d'Aosta", inplace = True)
   
   for regione in dati_regione['nome_area'].unique():
       
       vaccini_reg_day(dati_regione, regione, base)
       # vaccini cumulato regione (errore di conversione)
       # vaccini_reg_cum(dati_regione, regione, base)
       


def vaccini_reg_day(dati_regione, regione, base):
    df_reg = dati_regione.loc[dati_regione['nome_area'] == regione]    
       
    raggruppati = df_reg.groupby('data_somministrazione').sum().reset_index()
    raggruppati.index = pd.DatetimeIndex(raggruppati['data_somministrazione'])
    idx = pd.date_range(np.min(raggruppati.index), np.max(raggruppati.index))
    raggruppati = raggruppati.reindex(idx, fill_value = 0)
    
    
    raggruppati['prima_dose_ma'] = (raggruppati['prima_dose']+raggruppati['seconda_dose']).rolling(window = 7).mean()
    raggruppati['seconda_dose_ma'] = raggruppati['seconda_dose'].rolling(window = 7).mean()
    
    date = np.linspace(0,len(raggruppati['data_somministrazione'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 
    
    # vaccini giornalieri
    fig, ax = plt.subplots()
 
    plt.plot(date, raggruppati['prima_dose']+raggruppati['seconda_dose'], color='forestgreen', alpha = 0.7)
    plt.plot(date, raggruppati['seconda_dose'], color='gray', alpha = 0.7)
 
    l1 = plt.scatter(x = date[-1], y = raggruppati['prima_dose'].tail(1) + raggruppati['seconda_dose'].tail(1), color = "forestgreen", alpha = 1)
    l2 = plt.scatter(x = date[-1], y = raggruppati['seconda_dose'].tail(1), color = "gray", alpha = 1)
    l3 = Rectangle((0, 0), 1, 1, fc="w", fill=False, edgecolor='none', linewidth=0)
 
    x = ax.lines[-1].get_xdata()
    y = ax.lines[-1].get_ydata()
    y1 = ax.lines[-2].get_ydata()
 
    ax.fill_between(x, y, y1, color='forestgreen', alpha=0.3)
    ax.fill_between(x, 0, y, color='gray', alpha=0.3)
 
    plt.plot(date, raggruppati['prima_dose_ma'], color = "forestgreen", alpha = 1, linewidth =2)
    plt.plot(date, raggruppati['seconda_dose_ma'], color = "gray", alpha = 1, linewidth =2)

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
    plt.title(f"Somministazioni vaccini - {regione}", size = 15)
    lg = plt.legend([l1, l2, l3], ["Prima dose: {}".format(round(raggruppati['prima_dose'].tail(1).values[0],2)), 
                            "Seconda dose: {}".format(round(raggruppati['seconda_dose'].tail(1).values[0],2)),
                            "Tot. somministrazioni: {} mln".format(round((raggruppati['prima_dose'].sum() + raggruppati['seconda_dose'].sum())/1e+06,3))])
    
    plt.grid(alpha = 0.5)
    #plt.show()
    fig.savefig(f"pics/vaccini/day/{regione.lower()}.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
    plt.close(fig)
    

def vaccini_reg_cum(dati_regione, regione, base):
   df_platea = pd.read_csv("data/vaccini_platea.csv", sep = ',')
   pop_reg = df_platea[df_platea['nome_area'] == regione]['totale_popolazione'].sum() # fonte istat
   df_reg = dati_regione.loc[dati_regione['nome_area'] == regione] 
   
   raggruppati = df_reg.groupby('data_somministrazione').sum().reset_index()
   date = np.linspace(0,len(raggruppati['data_somministrazione'].unique()), len(raggruppati))
   date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 
   # somme cumulate
   raggruppati['prima_dose'] = (raggruppati['prima_dose'].cumsum()/pop_reg) * 100
   raggruppati['seconda_dose'] = (raggruppati['seconda_dose'].cumsum()/pop_reg) * 100
   
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
   plt.ylabel("Popolazione vaccinata", size = 12)
   
   fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
   yticks = mtick.FormatStrFormatter(fmt)
   ax.yaxis.set_major_formatter(yticks)
   plt.xticks(size = 10)
   
   plt.yticks(size = 10)
   plt.title(f"Percentuale vaccini - {regione}", size = 15)
   lg = plt.legend([l1, l2], ["Prima dose: {}%".format(round(raggruppati['prima_dose'].tail(1).values[0],2)), 
                           "Seconda dose: {}%".format(round(raggruppati['seconda_dose'].tail(1).values[0],2))])
   plt.grid(alpha = 0.5)
   fig.savefig(f"pics/vaccini/cum/{regione}.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')
   plt.close(fig)

