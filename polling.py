"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import  Updater
from telegram_dispatcher import get_dispatcher

# ------- Loggging-----------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

try:
    from config import TOKEN
    logger.info("config.py found")
except ImportError:
    import os
    logger.info("config.py not found, taking token from system variables")
    TOKEN = os.getenv("TOKEN")

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher = get_dispatcher(dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
