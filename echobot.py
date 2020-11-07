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

import logging
import nltk, re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from preprocessing.preprocessing import preprocess_data
from plot.plot_producer import plot_producer
# per thread e scheduler
from threading import Thread
import schedule
from time import sleep
from datetime import datetime as dt



def set_up():
    # global variables
    global token
    global logger
    global regions
    global dir_pics
    global s_date
    
    # To plot console log file
    # Enable logging
    logging.basicConfig(
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
    s_date = dt.strftime(dt.today(), "%d %h %Y %H:%M")
    # start update thread 
    t_sched = Thread(target = schedule_checker, args = [])
    t_sched.start()

# controllore se attivare o meno il thread
def schedule_checker():
    schedule.every().day.at('17:15').do(update_data, )
    while(True):
        schedule.run_pending()
        sleep(1)

# funzione update dei dati
def update_data():
    logging.info("Updating data ... ")
    preprocess_data()
    logging.info("Updating plots ... ")
    plot_producer()
    logging.info("Plots successfully updated!")
    return

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Ciao! Sono CovidItaliaNews_bot, spero di darti buone notizie oggi!' +
    '\nSono un grande esperto dei dati della pandemia che stiamo vivendo.\n' +
    'Chiedimi pure quello che vuoi :)\n\n' +
    'Se sei in difficoltà usa il comando /help')


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
            open(f"{dir_pics}/tamponi/{region}.png", "rb"),
            open(f"{dir_pics}/rapporto_tamponi/{region}.png", "rb"),
            open(f"{dir_pics}/ricoverati/{region}.png", "rb"),
            open(f"{dir_pics}/guariti/{region}.png", "rb"),
            open(f"{dir_pics}/terapia/{region}.png", "rb")]
        return l
    else:
        return None

def news_regions_recent(text_token):
    region = untokenize(text_token)
    if region in regions: #if region is correct
        l = [open(f"{dir_pics}/nuovi_positivi_news/{region}.png", "rb"),
            open(f"{dir_pics}/morti_news/{region}.png", "rb"),
            open(f"{dir_pics}/tamponi_news/{region}.png", "rb"),
            open(f"{dir_pics}/rapporto_tamponi_news/{region}.png", "rb"),
            open(f"{dir_pics}/ricoverati_news/{region}.png", "rb"),
            open(f"{dir_pics}/guariti_news/{region}.png", "rb"),
            open(f"{dir_pics}/terapia_news/{region}.png", "rb")]
        return l
    else:
        return None

def news(update):
    update.message.reply_text("Ecco la panoramica sui dati d'Italia del Covid-19 aggiornata al " + s_date) #### 
    update.message.reply_photo(open(f"{dir_pics}/nuovi_positivi/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/morti/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/tamponi/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/terapia/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/guariti/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/ricoverati/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/rapporto_tamponi/italia.png", "rb"))

def news_recent(update):
    update.message.reply_text("Ecco la panoramica sui dati d'Italia del Covid-19 aggiornata al " + s_date) #### 
    update.message.reply_photo(open(f"{dir_pics}/nuovi_positivi_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/morti_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/tamponi_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/terapia_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/guariti_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/ricoverati_news/italia.png", "rb"))
    update.message.reply_photo(open(f"{dir_pics}/rapporto_tamponi_news/italia.png", "rb"))
    
def echo(update, context):
    """Echo the user message."""
    #update.message.reply_text(update.message.text)
    text = update.message.text
    # preprocess del messaggio
    text = preprocess_text(text)
    # tokenize
    text_token = nltk.word_tokenize(text)

    if text == "ciao":
        update.message.reply_text("Ciao bello! Niente sintomi oggi?")
    elif text == "ciao sono fede":
        update.message.reply_text("Ciao padron Fede, lo sai che sei proprio bellissimo. Accarezza Diesel per me <3")
    elif text == "ciao sono chri":
        update.message.reply_text("Ciao padron Chri, lo sai che oggi hai proprio un bel aspetto. Salutami Buddy e Zoe <3")
    
    # update
    elif text == "chri e fede ti ordinano di aggiornarti":
        update.message.reply_text("Zi padrone!") 
        update.message.reply_text("Mi lasci il tempo di far lavorare gli schiavi e faccio tutto padrone.") 
        update.message.reply_text("...")
        update_data()
        # update timedata
        s_date = dt.strftime(dt.today(), "%d %h %Y %H:%M")
        update.message.reply_text("Finito padrone!\nQuesta volta sono morti solo in 3 schiavi padrone!") 
        update.message.reply_text("Mando gli ultimi dati aggiornati padrone <3")
        news(update)

    # news
    elif text_token[0] == "news":
        if len(text_token) == 1:
            news(update)
        elif text_token[1] == "recenti":
            if len(text_token) == 2:
                news_recent(update)
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
            region = check_region(text_token[2:])
            send_region(update, "deceduti_news", region)
        else:
            region = check_region(text_token[1:])
            send_region(update, "morti", region)
    
    # nuovi_positivi
    elif text_token[0] == "positivi":
        if len(text_token) == 1: #se non ha aggiunto nulla
            update.message.reply_photo(open(f"{dir_pics}/nuovi_positivi/italia.png", "rb"))
        elif text_token[1] == "recenti":
            region = check_region(text_token[2:])
            send_region(update, "positivi_news", region)
        else:
            region = check_region(text_token[1:])
            send_region(update, "nuovi_positivi", region)
    
    # rapporto tamponi
    elif text_token[0] == "rapporto" and text_token[1] == "tamponi":
        if len(text_token) == 2: #se non ha aggiunto nulla
            update.message.reply_photo(open(f"{dir_pics}/rapporto_tamponi/italia.png", "rb"))
        elif text_token[2] == "recenti":
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
            region = check_region(text_token[2:])
            send_region(update, "guariti_news", region)
        else:
            region = check_region(text_token[1:])
            send_region(update, "guariti", region)

    # se non è stato compreso il messsaggio    
    else:
        update.message.reply_text("Mi spiace non sono ancora in grado di capire quello che mi hai scritto.\nImparo pian piano!\n\nSe non sai cosa posso capire apri la guida con /help.")
    
    logger.info("Replyed to: " + str(text))


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

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()