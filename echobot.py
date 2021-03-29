#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

################################################################################
# update.message.chat_id # per avere la chat id
# per mandare messaggi mirati
#    context.bot.send_message(chat_id=<insert chat_id>)
################################################################################

import logging
import nltk, re
import requests
import pandas as pd
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from preprocessing.preprocessing import preprocess_data
from plot.plot_producer import plot_producer
# per thread e scheduler
from threading import Thread
import schedule
from time import sleep
from datetime import datetime as dt
from datetime import time, timedelta

def set_up():
    # global variables
    global token
    global logger
    global regions
    global dir_pics
    global s_date
    global t_sched
    
    # To plot console log file
    # Enable logging
    logging.basicConfig(
        filename='history.log', 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    logger = logging.getLogger(__name__)
    dir_pics = "pics"
    # read token_key and start bot
    with open("bot/token_key.txt", "r") as file:
        token = file.read()
    assert(token)
    # read regions file
    regions = []
    with open("bot/regioni.txt", "r") as file:
        line = file.readline()
        while line:
            l = line.rstrip() #remove '\n'
            regions.append(l)
            line = file.readline()
    # start str date
    s_date = dt.strftime(dt.today()+timedelta(hours=2), "%d %h %Y %H:%M")
    # start update scraping thread 
    t_sched = Thread(target = schedule_checker, args = [])
    t_sched.start()
    

# controllore se attivare o meno il thread
def schedule_checker():
    schedule.every().day.at('15:20').do(shedule_update, )
    while(True):
        schedule.run_pending()
        sleep(1)

# funzione update dei dati
def update_data(force = False):
    global s_date

    logging.info("Updating data ... ")
    flag = preprocess_data(force)
    # if data not updated
    while (not force) and (not flag):
        logging.warning("Data not update yet - waiting ...")
        sleep(100)
        flag = preprocess_data()

    logging.info("Updating plots ... ")
    plot_producer()
    s_date = dt.strftime(dt.today()+timedelta(hours=2), "%d %h %Y %H:%M")
    logging.info("Plots successfully updated!")


# schedule function
def shedule_update():
    update_data(force = False)
    personal_updates()

# send personal message
def personal_update(chat_id, name, sub):
    try:
        if sub == 1:
            URL = "https://api.telegram.org/bot{}/".format(token)
            text = f"Hey {name}! I dati sono stati aggiornati. Chiedimi quello che vuoi. \n\n Se non sai cosa puoi chiedermi digita /help"
            url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
        
            requests.post(url)
    except:
        logger.error(f'Error send personal message: chat_id: {chat_id} , name: {name}')

# send personal message to everyone
def personal_updates():
    df_chat_id = pd.read_csv('data/chat_id.csv', sep = ',')
    df_chat_id.apply(lambda x: personal_update(x['chat_id'], x['name'], x['sub']), axis = 1) 
    logger.info('Send updates to everyone')

# user registration
def personal_registration(chat_id, name, username, update):
    df_chat_id = pd.read_csv('data/chat_id.csv', sep = ',')
    # if user already registered
    if (df_chat_id['chat_id'] == chat_id).any(): # if user already registered
        if df_chat_id[df_chat_id['chat_id'] == chat_id]['sub'].values[0] == 1 :
            update.message.reply_text(f"Caro/a {name}, sei già registrato/a <3\n\nRiceverai la nostra notifica tutti i giorni")
            logger.warning(f'User {name} already registered')
        else: # if user comes back to register
            df_chat_id.at[df_chat_id['chat_id'] == chat_id,'sub'] = 1
            df_chat_id.to_csv('data/chat_id.csv', index = False)
            update.message.reply_text(f"Caro/a {name}, grazie per essere tornato/a <3\n\nRiceverai la nostra notifica tutti i giorni")
            logger.warning(f'User {name} already registered')
    else:
        # if no registered
        df_chat_id = df_chat_id.append({'chat_id':chat_id, 'name':name, 'username':username, 'sub':1}, ignore_index=True)
        df_chat_id.to_csv('data/chat_id.csv', index = False)
        update.message.reply_text(f"Caro/a {name}, ora sei registrato/a <3\n\nRiceverai la nostra notifica tutti i giorni, grazie di averci scelto!!")
        logger.info(f'User {name} correctly registered')

def personal_un_registration(chat_id, name, update):
    df_chat_id = pd.read_csv('data/chat_id.csv', sep = ',')

    if (df_chat_id['chat_id'] == chat_id).any(): # if user exists
        if df_chat_id[df_chat_id['chat_id'] == chat_id]['sub'].values[0] == 1: # if user is registered
            df_chat_id.at[df_chat_id['chat_id'] == chat_id,'sub'] = 0
            df_chat_id.to_csv('data/chat_id.csv', index = False)
            update.message.reply_text(f"Caro/a {name}, ci spiace che abbia deciso di disiscriverti </3\n\nPuoi comunque sempre utilizzare il bot e quando vorrai tornare ti basterà chiedere \"iscrivimi\" o /help")
            logger.info(f'User {name} unsubscribed')
        else: # if user already unregistered
            update.message.reply_text(f"Caro/a {name}, avevi già deciso di disiscriverti </3\n\nPuoi comunque sempre utilizzare il bot e quando vorrai tornare ti basterà chiedere \"iscrivimi\" o /help")
            logger.warning(f'User {name} already unsubscribed')
    else:
        update.message.reply_text(f"Caro/a {name}, non ti sei mai iscritto/a </3\n\nIscriviti tramite il comando \"iscrivimi\". Puoi comunque sempre utilizzare il bot")
        logger.warning(f'User {name} never subscribed')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Ciao! Sono CovidItaliaNews_bot, spero di darti buone notizie oggi!' +
    '\nSono un grande esperto dei dati della pandemia che stiamo vivendo.\n' +
    'Chiedimi pure quello che vuoi :)\n\n' +
    'Per ricevere la notifica giornaliera digita \"iscrivimi\"')
    help_command(update, context)
    update.message.reply_text("Ricordati che in ogni momento puoi vedere ciò che puoi chiedermi tramite /help")

# send messages to one master
def send_to_master(chat_id, name, message, update):
        try:
            URL = "https://api.telegram.org/bot{}/".format(token)
            url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(message, chat_id)
        
            requests.post(url)

        except:
            logger.error(f'Error send master message: chat_id: {chat_id} , name: {name}')
            
        logger.info(f'Send master message to {name}')

# send message to masters
def send_to_masters(message, update):
    df_chat_id = pd.read_csv('data/master_chat_id.csv', sep = ',')
    
    df_chat_id.apply(lambda x: send_to_master(x['chat_id'], x['name'], message, update), axis = 1)

def help_command(update, context):
    """Send a message when the command /help is issued."""
    help_text = ""
    with open("bot/commands.txt", "r") as file:
        help_text = file.read()
    update.message.reply_text(help_text)

def preprocess_text(text):
    text = text.lower()
    # aggiungere eventuale preprocess del testo
    return text

def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()

# input ho i token delle regioni
# output nome regione come stringa
def check_region(text_token):
    region = untokenize(text_token)
    if region in regions:
        return region
    else:
        return None

# input update manager, dir_kind (tipo di grafico - path), region
# output niente
def send_region(update, dir_kind, region):
    if region:
        update.message.reply_photo(open(f"{dir_pics}/{dir_kind}/{region}.png", "rb"))
    else:
        update.message.reply_text("!! Attenzione !! - Nome regione non corretto")

def news_regions(text_token):
    region = untokenize(text_token)
    if region in regions: #if region is correct
        l = [open(f"{dir_pics}/nuovi_positivi/{region}.png", "rb"),
            open(f"{dir_pics}/morti/{region}.png", "rb"),
            open(f"{dir_pics}/guariti/{region}.png", "rb"),
            open(f"{dir_pics}/rapporto_tamponi/{region}.png", "rb"),
            open(f"{dir_pics}/tamponi/{region}.png", "rb"),
            open(f"{dir_pics}/ricoverati/{region}.png", "rb"),
            open(f"{dir_pics}/terapia/{region}.png", "rb")
            ]
        return l
    else:
        return None

def news_regions_recent(text_token):
    region = untokenize(text_token)
    if region in regions: #if region is correct
        l = [open(f"{dir_pics}/nuovi_positivi_news/{region}.png", "rb"),
            open(f"{dir_pics}/morti_news/{region}.png", "rb"),
            open(f"{dir_pics}/guariti_news/{region}.png", "rb"),
            open(f"{dir_pics}/rapporto_tamponi_news/{region}.png", "rb"),
            open(f"{dir_pics}/tamponi_news/{region}.png", "rb"),
            open(f"{dir_pics}/ricoverati_news/{region}.png", "rb"),
            open(f"{dir_pics}/terapia_news/{region}.png", "rb")
            ]
        return l
    else:
        return None

def news_auto(context, chat_id):
    context.bot.send_message(chat_id = chat_id,
                text = "Ecco la panoramica sui dati d'Italia del Covid-19 aggiornata al " + s_date) ####         
    context.bot.sendPhoto(chat_id = chat_id, 
                photo = open(f"{dir_pics}/nuovi_positivi/italia.png", "rb"))
    context.bot.sendPhoto(chat_id = chat_id,
                photo = open(f"{dir_pics}/morti/italia.png", "rb"))  
    context.bot.sendPhoto(chat_id = chat_id,
                photo = open(f"{dir_pics}/guariti/italia.png", "rb"))
    context.bot.sendPhoto(chat_id = chat_id,
                photo = open(f"{dir_pics}/rapporto_tamponi/italia.png", "rb"))
    context.bot.sendPhoto(chat_id = chat_id,
                photo = open(f"{dir_pics}/tamponi/italia.png", "rb"))
    context.bot.sendPhoto(chat_id = chat_id,
                photo = open(f"{dir_pics}/ricoverati/italia.png", "rb"))
    context.bot.sendPhoto(chat_id = chat_id,
                photo = open(f"{dir_pics}/terapia/italia.png", "rb")) 

def news(update):
    update.message.reply_text("Ecco la panoramica sui dati d'Italia del Covid-19 aggiornata al " + s_date) ####         
    update.message.reply_photo(open(f"{dir_pics}/nuovi_positivi/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/morti/italia.png", "rb"))  
    update.message.reply_photo(open(f"{dir_pics}/guariti/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/rapporto_tamponi/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/tamponi/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/ricoverati/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/terapia/italia.png", "rb"))    

def news_recent(update, context):
    update.message.reply_text("Ecco la panoramica sui dati d'Italia del Covid-19 aggiornata al " + s_date) #### 
    update.message.reply_photo(open(f"{dir_pics}/nuovi_positivi_news/italia.png", "rb"))  
    update.message.reply_photo(open(f"{dir_pics}/morti_news/italia.png", "rb"))     
    update.message.reply_photo(open(f"{dir_pics}/guariti_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/rapporto_tamponi_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/tamponi_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/ricoverati_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/terapia_news/italia.png", "rb"))
       
def echo(update, context):

    global s_date
    
    """Echo the user message."""
    chat_id = update.message.chat.id # user chat_id
    name = update.message.chat.first_name # user first_name
    username = update.message.chat.username  # username
    text = update.message.text # input text
    # preprocess del messaggio
    text = preprocess_text(text)
    # tokenize
    text_token = nltk.word_tokenize(text)

    if text == "ciao":
        update.message.reply_text(f"Ciao {name}!")
    elif text == "iscrivimi":
        personal_registration(chat_id, name, username, update)
    elif text == "disiscrivimi":
        personal_un_registration(chat_id, name, update)
    # update
    elif text == "schiavo aggiornati":
        update.message.reply_text("Mi lasci il tempo di scaricare i dati e di disegnare.") 
        update.message.reply_text("...")
        update_data(force = True)
        update.message.reply_text("Questi sono gli ultimi dati aggiornati")
        news(update)
    # update to everyone
    elif text == "schiavo manda messaggi a tutti":
        personal_updates()

    # news
    elif text_token[0] == "news":
        if len(text_token) == 1:
            news(update)
        elif text_token[1] == "recenti":
            if len(text_token) == 2:
                news_recent(update, context)
            else:
                region = news_regions_recent(text_token[2:])
                if region:
                    for photo in region:
                        update.message.reply_photo(photo)
                else:
                    update.message.reply_text("!! Attenzione !! - Nome regione non corretto")
        
        else:
            region = news_regions(text_token[1:])
            if region:
                for photo in region:
                    update.message.reply_photo(photo)
            else:
                update.message.reply_text("!! Attenzione !! - Nome regione non corretto")

    # terapia intensiva
    elif text_token[0] == "terapia" and text_token[1] == "intensiva":
        if len(text_token) == 2: #se non ha aggiunto nulla
            update.message.reply_photo(open("pics/terapia/italia.png", "rb"))
        elif text_token[2] == "recenti":
            if len(text_token) == 2: #se non ha aggiunto nulla
                update.message.reply_photo(open("pics/terapia_news/italia.png", "rb"))
            else:
                region = check_region(text_token[3:])
                send_region(update, "terapia_news", region)
        else:
            region = check_region(text_token[2:])
            send_region(update, "terapia", region)
    # deceduti
    elif text_token[0] == "deceduti":
        if len(text_token) == 1: #se non ha aggiunto nulla
            update.message.reply_photo(open(f"{dir_pics}/morti/italia.png", "rb"))
        elif text_token[1] == "recenti":
            if len(text_token) == 2: #se non ha aggiunto nulla
                update.message.reply_photo(open("pics/morti_news/italia.png", "rb"))
            else:
                region = check_region(text_token[2:])
                send_region(update, "morti_news", region)
        else:
            region = check_region(text_token[1:])
            send_region(update, "morti", region)
    
    # nuovi_positivi
    elif text_token[0] == "positivi":
        if len(text_token) == 1: #se non ha aggiunto nulla
            update.message.reply_photo(open(f"{dir_pics}/nuovi_positivi/italia.png", "rb"))
        elif text_token[1] == "recenti":
            if len(text_token) == 2: #se non ha aggiunto nulla
                update.message.reply_photo(open("pics/nuovi_positivi_news/italia.png", "rb"))
            else:
                region = check_region(text_token[2:])
                send_region(update, "nuovi_positivi_news", region)
        else:
            region = check_region(text_token[1:])
            send_region(update, "nuovi_positivi", region)
    
    # rapporto tamponi
    elif text_token[0] == "rapporto" and text_token[1] == "tamponi":
        if len(text_token) == 2: #se non ha aggiunto nulla
            update.message.reply_photo(open(f"{dir_pics}/rapporto_tamponi/italia.png", "rb"))
        elif text_token[2] == "recenti":
            if len(text_token) == 3: #se non ha aggiunto nulla
                update.message.reply_photo(open("pics/rapporto_tamponi_news/italia.png", "rb"))
            else:
                region = check_region(text_token[3:])
                send_region(update, "rapporto_tamponi_news", region)
        else:
            region = check_region(text_token[2:])
            send_region(update, "rapporto_tamponi", region)
    
    # tamponi
    elif text_token[0] == "tamponi":
        if len(text_token) == 1: #se non ha aggiunto nulla
            update.message.reply_photo(open(f"{dir_pics}/tamponi/italia.png", "rb"))
        elif text_token[1] == "recenti":
            if len(text_token) == 2: #se non ha aggiunto nulla
                update.message.reply_photo(open("pics/tamponi_news/italia.png", "rb"))
            else:
                region = check_region(text_token[2:])
                send_region(update, "tamponi_news", region)
        else:
            region = check_region(text_token[1:])
            send_region(update, "tamponi", region)

    # ricoverati
    elif text_token[0] == "ricoverati":
        if len(text_token) == 1: #se non ha aggiunto nulla
            update.message.reply_photo(open(f"{dir_pics}/ricoverati/italia.png", "rb"))
        elif text_token[1] == "recenti":
            if len(text_token) == 2: #se non ha aggiunto nulla
                update.message.reply_photo(open("pics/ricoverati_news/italia.png", "rb"))
            else:
                region = check_region(text_token[2:])
                send_region(update, "ricoverati_news", region)
        else:
            region = check_region(text_token[1:])
            send_region(update, "ricoverati", region)
    
    # guariti
    elif text_token[0] == "guariti":
        if len(text_token) == 1: #se non ha aggiunto nulla
            update.message.reply_photo(open(f"{dir_pics}/guariti/italia.png", "rb"))
        elif text_token[1] == "recenti":
            if len(text_token) == 2: #se non ha aggiunto nulla
                update.message.reply_photo(open("pics/guariti_news/italia.png", "rb"))
            else:
                region = check_region(text_token[2:])
                send_region(update, "guariti_news", region)
        else:
            region = check_region(text_token[1:])
            send_region(update, "guariti", region)

    # se non è stato compreso il messsaggio    
    else:
        update.message.reply_text("Mi spiace non sono ancora in grado di capire quello che mi hai scritto.\nImparo pian piano!\n\nSe non sai cosa posso capire apri la guida con /help.")
    
    logger.info(f"Ask {name}: " + str(text))


def main():
    """Start the bot."""
    set_up()
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    
    # daily update handler
    #j = updater.job_queue
    #job.run_daily(update_data, time(hour=12, minute=12))
 
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    
    #j.run_daily(update_data, time(hour=12, minute=12))
    
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
