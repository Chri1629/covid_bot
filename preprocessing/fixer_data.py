import pandas as pd

def fix_datasets():
    dati = pd.read_csv("data/dati_regioni.csv")
    regioni = pd.read_csv("data/regioni.csv")

    ## Devo mergiare i dati del trentino
    dati.drop(columns = ["casi_da_sospetto_diagnostico", "casi_da_screening"], axis = 1, inplace = True)
    dati.dropna(thresh = 3, inplace = True)

    df_r = dati.loc[(dati['denominazione_regione'] == "P.A. Bolzano") | (dati['denominazione_regione'] == "P.A. Trento")]
    df_trentino = df_r.groupby("data").sum()
    df_trentino['denominazione_regione'] = "Trentino Alto Adige" 

    df_trentino['lat'] = 46.068935
    df_trentino['long'] = 11.121231
    df_trentino = df_trentino.reset_index()
    dati = dati.loc[(dati['denominazione_regione'] != "P.A. Trento") & (dati['denominazione_regione'] != "P.A. Bolzano")]

    dati_fix = pd.concat([dati, df_trentino], sort=False)
    dati_fix['stato'] = "ITA"
    dati_fix = dati_fix.drop(dati_fix[["note"]], axis=1)

    dati_correct = pd.merge(dati_fix, regioni, left_on = 'denominazione_regione', right_on = 'regione')
    dati_correct = dati_correct.drop('denominazione_regione', axis = 1)

    dati.to_csv("data/dati_regioni.csv")
    dati_correct.to_csv("data/dati.csv")
    print("Dataset Regioni fixed")
    # ***
    # Province
    dati_p = pd.read_csv("data/dati_province.csv")
    #i in fase di definizione sono inutili
    #dati_p = dati_p[dati_p['denominazione_provincia'] != "In fase di definizione/aggiornamento"] # drop in fase di aggiornamento
    pd.set_option('mode.chained_assignment', None)
    df_tb = dati_p.loc[(dati_p['denominazione_regione'] == "P.A. Bolzano") | (dati_p['denominazione_regione'] == "P.A. Trento")]
    df_tb.loc['denominazione_regione'] = "Trentino Alto Adige"
    #sistemo nome provincia di Aosta in Valle d'Aosta così lo prende tableau
    dati_p["denominazione_provincia"][dati_p['denominazione_regione'] == "Valle d'Aosta"] = "Valle d'Aosta"
    dati_p[dati_p['codice_regione'] == 2]
    #tolgo i dati del Trentino
    dati_p = dati_p.loc[(dati_p['denominazione_regione'] != "P.A. Trento") & (dati_p['denominazione_regione'] != "P.A. Bolzano")]

    dati_p_fix = pd.concat([dati_p, df_tb], sort=False)
    dati_p_fix = dati_p_fix.drop(dati_p_fix[["note"]], axis=1)
    #dati_p_fix[dati_p_fix["codice_regione"] == 4]
    #dati_p_fix = dati_p_fix[dati_p_fix["denominazione_provincia"] != "Fuori Regione / Provincia Autonoma"]
    
    dati_p_fix.to_csv("data/dati_p.csv")
    print("Dataset Province fixed")