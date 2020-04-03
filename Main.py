import logging
import threading
import sys
import signal
from time import sleep

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = '<Token>'
CHAT_ID = -1
IDLE_SLEEP_S = 1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def bot_start(update, context):
    """On command /start

    :param update: Update
    :param context: Context
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='Hi, I\'m Raspi Surveillance Bot!')


def bot_help(update, context):
    """On command /help

    :param update: Update
    :param context: Context
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='This is the Raspi Surveillance Bot.')


def bot_echo(update, context):
    """On text

    :param update: Update
    :param context: Context
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def bot_unknown(update, context):
    """On command not found

    :param update: Update
    :param context: Context
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


def bot_error(update, context):
    """On errors

    :param update: Update
    :param context: Context
    """
    logging.warning('Update "%s" caused error "%s"', update, context.error)


def bot_init():
    """Initializes the bot"""
    logging.info('Initializing')

    updater = Updater(token=TOKEN, use_context=True)

    return updater


def bot_register_handlers(updater):
    """Registers the bot handlers

    :param updater: The updater
    """
    logging.info('Registering handlers')

    if not updater:
        logging.error('Updater not set')
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    start_handler = CommandHandler('start', bot_start)
    help_handler = CommandHandler('help', bot_help)

    # on noncommand i.e message - echo message/unknown command message
    echo_handler = MessageHandler(Filters.text, bot_echo)
    unknown_handler = MessageHandler(Filters.command, bot_unknown)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(unknown_handler)

    # log all errors
    dispatcher.add_error_handler(bot_error)

    return updater


def bot_start_polling(updater, idle=False):
    """Starts polling

    :param updater: The updater
    :param idle: Whether to idle via telegram bot API, default: False
    """
    if updater:
        logging.info('Starting polling')

        # Start the Bot
        updater.start_polling(timeout=1.0)

        if idle:
            logging.info('Idleing via updater...')
            # Run the bot until you press Ctrl-C or the process receives SIGINT,
            # SIGTERM or SIGABRT. This should be used most of the time, since
            # start_polling() is non-blocking and will stop the bot gracefully.
            updater.idle()
    else:
        logging.error('Updater not set, could not start polling')


def bot_stop(updater):
    """Stops the bot

    :param updater: The updater
    """
    if updater:
        logging.info('Stopping dispatcher')
        updater.dispatcher.stop()
        logging.info('Stopping updater')
        updater.stop()
        updater.is_idle = False


class GracefulKiller:

    def __init__(self):
        """Initializes the graceful killer state"""
        self.kill_now = False
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)

    def _exit_gracefully(self, signum, frame):
        """Sets the graceful killer state to exit

        :param signum The exit signal
        :param frame: The frame
        """
        logging.info('Received exit signal {}'.format(signum))
        self.kill_now = True


if __name__ == '__main__':
    bot_up = False
    try:
        bot_updater = bot_init()
        bot_register_handlers(bot_updater)
        bot_start_polling(bot_updater, idle=False)
        bot_up = True
    except Exception as e:
        logging.error(e)
        bot_up = False

    if not bot_up:
        bot_stop(bot_updater)
        logging.error('Bot is not up. Exiting.')
        sys.exit(0)

    logging.info('Successfully started.')

    bot = telegram.Bot(token=TOKEN)
    bot_info = bot.get_me()
    logging.info('Bot info: {}'.format(bot_info))
    logging.info('Sending messages to chat[ID={}]'.format(CHAT_ID))

    g_killer = GracefulKiller()
    while not g_killer.kill_now:
        try:
            inputStr = input('{}@{}> '.format(bot_info['username'], CHAT_ID))
            if inputStr:
                bot.send_message(chat_id=CHAT_ID, text=inputStr)
        except:
            g_killer.kill_now = True
        sleep(IDLE_SLEEP_S)

    """
    Comment in to send an image
    bot.send_message(chat_id=CHAT_ID, text='New image taken')
    bot.send_photo(chat_id=CHAT_ID, photo=open('test-img.png', 'rb'))
    """


    bot_stop(bot_updater)
    logging.info('Exiting')
    sys.exit(0)
