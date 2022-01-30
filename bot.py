"""
A conversa com o bot inicia com /nomedobot e finaliza com /tchau. 
"""

"""
Na linha 41 tem umas constantes, tu pode adicionar mais e mudar o range se adicionar.
Elas tu usa de retorno pq encaminha o fluxo do chat, tipo nomedobot -> flows -> options.
isso tu configura dentro da função main onde tem justamente essas constante e a chamada para função.

ficou faltando:
2. Quero saber se minha rota está tranquila
3. Quero saber qual o melhor horário para passar pela minha rota


"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Ativa logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

SAFETY, FLOWS, OPTIONS, PHOTO, ANSWER, LOCATION = range(6)

def lelibot(update: Update, context: CallbackContext) -> int:
    """Inicia a conversa e pergunta ao usuário sobre sua segurança."""

    reply_keyboard = [['Sim', 'Não']]

    update.message.reply_text(
        'aqui é a Lê! Vou iniciar uma conversa com você. '
        'Envie /tchau para parar de falar comigo.\n\n'
        'Você está segura?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Sim ou Não?'
        ),
    )

    return FLOWS


def flows(update: Update, context: CallbackContext) -> int:
    """Pede as opções ou pergunta sobre compartilhar localização."""

    user = update.message.from_user
    logger.info("Safety of %s: %s", user.first_name, update.message.text)

    if update.message.text == "Sim":

        reply_keyboard = [['1', '2', '3']]

        update.message.reply_text(
            'fico tranquila que esteja segura! me conta como posso te ajudar? \n\n'
            'Opções:\n'
            '1. Quero registrar um novo local de vulnerabilidade\n'
            '2. Quero saber se minha rota está tranquila\n'
            '3. Quero saber qual o melhor horário para passar pela minha rota',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='1, 2 ou 3?'
            ),
        )

        return OPTIONS
    
    # update.message.text == "Não":

    reply_keyboard = [['Sim', 'Não']]

    update.message.reply_text(
        'não se preocupe, eu vou te ajudar!\n '
        'Você gostaria de compartilhar sua localização comigo?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Sim ou Não?'
        ),
    )

    return ANSWER


def options(update: Update, context: CallbackContext) -> int:
    """encaminha para outras funcoes de acordo com a opcao"""

    user = update.message.from_user
    logger.info("Option choice of %s: %s", user.first_name, update.message.text)

    if update.message.text == "1":

        update.message.reply_text(
            'Por favor me mande uma foto do local.'
        )
        
        return PHOTO

    elif update.message.text == "2": # nao faço ideia de como implementar isso

        update.message.reply_text('Em breve! Ainda estamos em desenvolvimento.')
        
        
    elif update.message.text == "3": # mar brilha aqui please
        
        update.message.reply_text('Em breve! Ainda estamos em desenvolvimento.')

    update.message.reply_text('Conversa finalizada. para iniciar uma nova conversa basta escrever /lelibot.')

    return ConversationHandler.END


def photo(update: Update, context: CallbackContext) -> int:
    """Armazena a foto"""

    import uuid

    user = update.message.from_user
    photo_id = str(uuid.uuid4())

    photo_file = update.message.photo[-1].get_file()
    photo_file.download(f'{photo_id}.jpg')

    logger.info("Photo of %s id: %s", user.first_name, f'{photo_id}')

    update.message.reply_text(
            'Foto recebida. para iniciar uma nova conversa basta escrever /lelibot.'
    )

    return ConversationHandler.END


def answer(update: Update, context: CallbackContext) -> int:
    """encaminha para funções de ação maior."""

    user = update.message.from_user
    logger.info("Answer choice of %s: %s", user.first_name, update.message.text)

    if update.message.text == "Sim":

        update.message.reply_text(
            'Por favor me mande sua localização.'
        )

        return LOCATION
    
    update.message.reply_text(
        'Obrigada! Espero que possamos conversar novamente algum dia. para iniciar uma nova conversa basta escrever /lelibot.'
    )

    return ConversationHandler.END


def location(update: Update, context: CallbackContext) -> int:
    """Armazena a localização"""

    user = update.message.from_user
    user_location = update.message.location

    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )

    with open("locations.txt", "a") as myfile:
        myfile.write(f'{user.first_name}, {user_location.latitude}, {user_location.longitude}\n')

    update.message.reply_text(
        'Obrigada! Espero que possamos conversar novamente algum dia. para iniciar uma nova conversa basta escrever /lelibot.'
    )

    return ConversationHandler.END


def tchau(update: Update, context: CallbackContext) -> int:
    """encerra a conversa."""

    user = update.message.from_user
    logger.info("User %s end the conversation.", user.first_name)

    update.message.reply_text(
        'Tchau! para iniciar uma nova conversa basta escrever /lelibot.', 
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


def main() -> None:
    """Run no bot."""

    import os
    PORT = int(os.environ.get('PORT', 5000))
    TOKEN = '5175975992:AAF9CKJFAuE_o6I6Hp90l1XupPypem8z3lE'

    # Create the Updater and pass it your bot's token.
    # global TOKEN
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('lelibot', lelibot), CommandHandler('start', lelibot)],
        states={
            FLOWS: [MessageHandler(Filters.regex('^(Sim|Não)$'), flows)],
            OPTIONS: [MessageHandler(Filters.regex('^(1|2|3)$'), options)],
            PHOTO: [MessageHandler(Filters.photo, photo)],
            ANSWER: [MessageHandler(Filters.regex('^(Sim|Não)$'), answer)],
            LOCATION: [MessageHandler(Filters.location, location)],
        },
        fallbacks=[CommandHandler('tchau', tchau)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://hackabot-telegram.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()