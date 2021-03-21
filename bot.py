from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import sys
import os
import requests
import json
from os import path
from os import remove
def start(update, context):
    try:
        message = "Bienvenido"
        update.message.reply_text(message)
    except Exception as error:
        print("Error /start: "+str(error.args[0]))
def echo(update, context):  
    try:  
        written = update.messsage.writen
        update.message.reply_text(written)
    except Exception as error:
        print("Error echo()"+str(error.args[0]))
def help(update, context):
    try:
        message = "Envia alguna Imagen de formato jpg o una opcion"
        update.message.reply_text(message)
    except Exception as error:
        print("Error /help: "+str(error.args[0]))
def fail(update, context, error):
    try:   
        print(error)
    except Exception as bug:
        print("Error in fail: "+str(bug.args[0]))
def sendImmage(update, context,bot): 
    try:
        received = "Leyendo imagen"
        update.message.reply_text(received)
        archive = bot.getFile(update.message.photo[-1].file_id)
        id = archive.file_id

        archive_save = os.path.join("imagenes/","{}.jpg".format(id))
        archive.download(archive_save)

        message = "Imagen almacenada con Exito"
        update.message.reply_text(message)

        archives = {"File":open(archive_save, "rb")}
        message = "Imagen en proceso"
        update.message.reply_text(message)
        result = requests.post("URL of api", archives = archives)

        get = result.json()
        things = get[list(get.keys()[0])]

        for i in things:
            title = i["result"]
            description = i["description"]

        message = "Resultado: "+title+"\n Description: "+description
        update.message.reply_text(message)

        if path.exists(archive_save):  
            remove(archive_save)
    except Exception as error:
        print("Error in sendImmage: "+str(error))
if __name__ == '__main__':
    #conexion al bot
    updater = Updater(token = "1671456103:AAHuwKEVzoLJGB8zLBIzacYooLjKDEZ7fR8", use_context=True )
    dp = updater.dispatcher
    #ejecuta la funcion de start
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help",help))
    #options 2
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, sendImmage))
        #error
    dp.add_error_handler(fail)
    updater.start_polling()
    updater.idle()
