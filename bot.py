import telepot 
import time
from telepot.loop import MessageLoop
from googletrans import Translator


#token access = 6806394373:AAFWy3UuhrIg9eQSNlkcegNcmz1VTsSQ9uQ
#link telegram = https://t.me/besto_translate_bot
bot = telepot.Bot('6806394373:AAFWy3UuhrIg9eQSNlkcegNcmz1VTsSQ9uQ')

target_languages = {}

def translate_text(textoo, target_language):
    translator = Translator()
    traduccion = translator.translate(textoo, dest=target_language)
    tranduccion_texto = traduccion.text if traduccion else 'no se ha podido traducir su texto'
    return tranduccion_texto

def procesoIdioma(msg):
    content_type, chat_type, chat_id = telepot.glance(msg) 
    
    if content_type == 'text':
        chatmsg = msg['text']
        """ translated_message = translate_text(message) no funca aquí
        bot.sendMessage(chat_id, f'Traducción: {translated_message}') """
        target_language = target_languages.get(chat_id, None)
        if chatmsg.lower() == '/spanish':
            bot.sendMessage(chat_id, 'Ahora traduciré del español al inglés.')
            #Establecer el idioma  como inglés
            target_languages[chat_id] = 'en'
            """ return """
            
        elif chatmsg.lower() == '/english':
            bot.sendMessage(chat_id, 'Now I will translate from English to Spanish.')
            #Establecer el idioma como español
            target_languages[chat_id] = 'es'
            
        elif chatmsg.lower() == '/default':
            bot.sendMessage(chat_id, 'Ahora no traduciré hasta que me indiques un idioma.')
            #idioma (ninguno)
            target_languages.pop(chat_id, None)
            
        else:
            
            if target_language:
                translated_message = translate_text(chatmsg, target_language)
                bot.sendMessage(chat_id, f'Traducción: {translated_message}')
            else:
                bot.sendMessage(chat_id, 'Por favor, establece un idioma de destino antes de enviar mensajes para traducir.')


        
MessageLoop(bot, procesoIdioma).run_as_thread()

while True:
    time.sleep(1)
