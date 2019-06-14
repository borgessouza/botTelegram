#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import requests
import sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

TAG_SEARCH='tagSearch/%23'
LOAD='carregar'
USER='user/tag'
LANG='lang'
DATA='data'


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
    retorno = requests.get(URI + LOAD )
    if retorno.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text='Carregado!!')

def users(bot, update):
    retorno = requests.get(URI + USER )
    if retorno.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text=retorno.text)

def lang(bot, update):
    retorno = requests.get(URI + LANG )
    if retorno.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text=retorno.text)

def data(bot, update):
    retorno = requests.get(URI + DATA )
    if retorno.status_code == 200:
        bot.send_message(chat_id=update.message.chat_id, text=retorno.text)

def echo(bot, update):
    text_answer = 'Oi?'
    bot.send_message(chat_id=update.message.chat_id, text=text_answer)

def encontrar_tags(bot, update):
    texto = update.message.text.replace('/tag','')
    texto = texto.replace(' ','')
    if texto:
        retorno = requests.get(URI + TAG_SEARCH + texto)
        bot.send_message(chat_id=update.message.chat_id, text=retorno.text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Favor Informa: /tag conteudo')

def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Ops Aconteceu um error "%s"', update.message)



def main():
    BOT_TOKEN = None

    if not BOT_TOKEN:
        print ('Favor preencher o token do Bot')
        sys.exit(1)

    updater = Updater(BOT_TOKEN)

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
    if len(sys.argv) < 3:
        print ('Favor preencher parametros: [Servidor porta]')
        sys.exit(1)
    else:
        SERVIDOR=sys.argv[1]
        PORTA=sys.argv[2]
        print('Utilizando:')
        URI='http://' + SERVIDOR + ':' + PORTA +  '/twitter/'
        print(URI)
        main()
