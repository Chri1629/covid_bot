import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

def create_report(file_log):
    # Legge i file
    dati = pd.read_csv(file_log)

    # Trasforma l'attributo data in un array in modo da poterlo disegnare
    date = np.linspace(0,len(dati['data'].unique()), len(raggruppati))
    date = np.array([base + dt.timedelta(days = i) for i in range(len(date))]) 

    # Vanno selezionati solo quelli che contengono le richieste
    dati_richieste = dati.loc[dati[-1] == "ASK"]
    # Vanno raggruppati per giorno in modo da contarli
    conteggi_giorno = dati.groupby("data").count().reset_index()

    # Disegna sull'asse temporale 
    fig, ax = plt.subplots()
    plt.plot(date, conteggi_giorno['count'], color = "#00a9c3", alpha = 0.8, linewidth =2)
    l1 = plt.scatter(x = date[-1], y = conteggi_giorno['count'].tail(1), color = "#00a9c3", alpha = 1)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.ylim(bottom = 0)
    plt.xlabel("Data", size = 12)
    plt.ylabel("Conteggi", size = 12)
    plt.xticks(size = 10)
    plt.yticks(size = 10)
    plt.title("Richieste mandate al bot")
    lg = plt.legend([l1], ["{}: {}\nsettimana:{}".format(date[-1].strftime("%d-%h"), int(conteggi_giorno['count'].tail(1).values[0]), 
    date[-2].strftime("%d-%h"), int(conteggi_giorno['count'].tail(2).values[0] + conteggi_giorno['count'].tail(3).values[0] + conteggi_giorno['count'].tail(4).values[0] +
    conteggi_giorno['count'].tail(5).values[0] + conteggi_giorno['count'].tail(6).values[0] + conteggi_giorno['count'].tail(7).values[0] +
    conteggi_giorno['count'].tail(8).values[0]))], 
    bbox_to_anchor=(1.01, 0.6, 1.1, 0.2), loc='upper left')
    plt.grid(alpha = 0.5)
    fig.savefig("pics/report/conteggio.png", dpi = 100, bbox_extra_artists=(lg,), bbox_inches='tight')

    pass