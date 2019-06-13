#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

URI='Http://localhost:8080/twitter/'
TAG_SEARCH='tagSearch/%23'




def start(bot, update):
    text_answer = 'Você já esta iniciado!'
    bot.send_message(chat_id=update.message.chat_id, text=text_answer)

def help(bot, update):
    text_answer = 'use: /tag -> Para procurar uma tag \n' \
    'use: /carregar -> Para carregar dados no cassandra \n'
    bot.send_message(chat_id=update.message.chat_id, text=text_answer)
    text_answer = 'use: /users -> Para trazer usuario com maior numero de twitts \n' \
    'use: /lang -> Para trazer o total para cada tag solicitada \n'
    bot.send_message(chat_id=update.message.chat_id, text=text_answer)
    text_answer = 'use: /data -> Para trazer postagens por hora e dia'
    bot.send_message(chat_id=update.message.chat_id, text=text_answer)

def carregar(bot, update):
    text_answer = 'carregando'
    bot.send_message(chat_id=update.message.chat_id, text=text_answer)
    retorno = requests.get(URI + 'carregar' )
    if retorno.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text='Carregado!!')

def users(bot, update):
    retorno = requests.get(URI + 'user/tag' )
    if retorno.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text=retorno.text)

def lang(bot, update):
    retorno = requests.get(URI + 'lang/pt' )
    if retorno.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text=retorno.text)

def data(bot, update):
    retorno = requests.get(URI + 'data' )
    if retorno.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text=retorno.text)

def echo(bot, update):
    text_answer = 'Oi?'
    bot.send_message(chat_id=update.message.chat_id, text=text_answer)

def encontrar_tags(bot, update):
    texto = update.message.text.replace('/tag ','')
    if texto:
        retorno = requests.get(URI + TAG_SEARCH + texto)
        bot.send_message(chat_id=update.message.chat_id, text=retorno.text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Favor Informa: /tag conteudo')

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update caused error "%s"', update.message)



def main():
   updater = Updater("894039799:AAF9KN2h8Uk9LbX6z9A3xqHLAPd_TGw-JHE")

   dp = updater.dispatcher

   dp.add_handler(CommandHandler("start", start))
   dp.add_handler(CommandHandler("help", help))
   dp.add_handler(CommandHandler("tag",encontrar_tags))
   dp.add_handler(CommandHandler("carregar", carregar))
   dp.add_handler(CommandHandler("users", users))
   dp.add_handler(CommandHandler("lang", lang))
   dp.add_handler(CommandHandler("data", data))
   dp.add_handler(CommandHandler("echo", echo))

   dp.add_handler(MessageHandler(Filters.text, echo))

   dp.add_error_handler(error)

   updater.start_polling()
   updater.idle()


if __name__ == '__main__':
    main()
