# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import csv, re
import pandas as pd
from datetime import datetime as dt

##################################################
# SCRAPING
################################################
page = requests.get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv")

data = page.content.decode('utf-8').splitlines()

#with open(r"C:\Users\fede9\Documents\GitHub\covid_bot\data\vaccini.csv", "w", encoding = "utf-8") as csv_file:
with open("../data/vaccini.csv", "w", encoding = "utf-8") as csv_file:
   writer = csv.writer(csv_file, delimiter = ",")
   for line in data:
       l = re.split(',', line)
       assert(len(l) == 19) # se il numero di campi per riga è corretto
       writer.writerow(l)
       

####################################################
# LOADING
##############################################


#df = pd.read_csv(r"C:\Users\fede9\Documents\GitHub\covid_bot\data\vaccini.csv", sep = ',')
df = pd.read_csv("../data/vaccini.csv", sep = ',')
# formato data
df['data_somministrazione']= pd.to_datetime(df['data_somministrazione'])

# NO Na
# drop useless columns
df['regione'] = df['nome_area'] # rename
df['data'] = df['data_somministrazione'] # rename
df = df.drop(['data_somministrazione', 'area', 'codice_NUTS1', 'nome_area', 'codice_NUTS2', 'codice_regione_ISTAT'], axis = 1)

# save
#df.to_csv(r"C:\Users\fede9\Documents\GitHub\covid_bot\data\vaccini_fixed.csv", index = False)
df.to_csv("../data/vaccini_fixed.csv", index = False)

#########################################################
# ANDAMENTO
########################################################
#df = pd.read_csv(r"C:\Users\fede9\Documents\GitHub\covid_bot\data\vaccini_fixed.csv")
df = pd.read_csv("../data/vaccini_fixed.csv")

df['data'] = pd.to_datetime(df['data'])
df_and = df[['data', 'prima_dose', 'seconda_dose']].copy()

df_and = df_and.groupby('data').sum()

from matplotlib import pyplot as plt
import seaborn as sns

plt.plot(df_and.index, df_and['prima_dose'])
plt.show()

##########################################################
# PLOT DI CHRI
###########################################################
#colonna = dati.columns[17]
colonna = "prima_dose"
fig, ax = plt.subplots(figsize=(8, 6))

sns.lineplot(x = df_and.index, y = df_and['prima_dose']+df_and['seconda_dose'], color='forestgreen', ax=ax)
sns.lineplot(x = df_and.index, y = df_and['seconda_dose'], color='gray', ax=ax)

x = ax.lines[-1].get_xdata()
y = ax.lines[-1].get_ydata()
y1 = ax.lines[-2].get_ydata()

ax.fill_between(x, y, y1, color='forestgreen', alpha=0.3)
ax.fill_between(x, 0, y, color='gray', alpha=0.3)

######### robe ##########################
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

pos_ticks = np.array([t for t in ax.get_yticks() if t > 0])
ticks = np.concatenate([-pos_ticks[::-1], [0], pos_ticks])

ax.set_yticks(ticks)
ax.set_yticklabels([f'{abs(t):.2f}' for t in ticks])
ax.spines['bottom'].set_position('zero')
plt.legend([],[], frameon=False)

plt.xlabel(r"Value (years)", horizontalalignment = "right", x=1.0, size = 15)
plt.yticks(size = 12)
plt.legend([],[], frameon=False)
plt.ylabel("Density of probability", fontsize = 15)
#plt.title("{}".format(colonna), fontsize = 20)
plt.title("Age", fontsize = 20)
plt.show()