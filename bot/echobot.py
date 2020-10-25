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
import telegram
import nltk, re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def set_up():
    # global variables
    global token
    global logger
    global regions
    # To plot console log file
    # Enable logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    # read token_key and start bot
    with open("token_key.txt", "r") as file:
        token = file.read()
    assert(token)
    regions = []
    with open("regioni.txt", "r") as file:
        line = file.readline()
        while line:
            l = line.rstrip() #remove '\n'
            regions.append(l)
            line = file.readline()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Ciao! Sono CovidItaliaNews_bot, spero di darti buone notizie oggi!' +
    '\nSono un grande esperto dei dati della pandemia che stiamo vivendo.\n' +
    'Chiedimi pure quello che vuoi :)')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

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

def terapia_intensiva_regions(text_token):
    region = untokenize(text_token[2:])
    if region in regions: #if region is correct
        return open(f"pics/terapia/terapia_{region}.png", "rb")
    else:
        return None

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
    elif text == "immagine prova":
        update.message.reply_text("Ora ti mando una bella foto del diesel!")
        update.message.reply_photo(open("pics/prova.jpg", "rb"))
    # terapia intensiva
    elif text_token[0] == "terapia" and text_token[1] == "intensiva":
        if len(text_token) == 2: #se non ha aggiunto nulla
            update.message.reply_photo(open("pics/terapia/terapia_intensiva.png", "rb"))
        else:
            region = terapia_intensiva_regions(text_token)
            if region:
                update.message.reply_photo(region)
            else:
                update.message.reply_text("!! Attenzione !! - Nome regione non corretto")
        
    else:
        update.message.reply_text("Mi spiace non sono ancora in grado di capire quello che mi hai scritto. Imparo pian piano!")
    
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