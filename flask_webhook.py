import json
import logging
from urllib.parse import urljoin

from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher

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
    from config import HOSTING_URL, TOKEN
    logger.info("config.py found")
except ImportError:
    import os
    logger.info("config.py not found, taking token from system variables")
    TOKEN = os.getenv("TOKEN")
    HOSTING_URL = os.getenv("HOSTING_URL")

app = Flask(__name__)


def main() -> None:

    # Create filter to check if a user is admin
    bot = Bot(TOKEN)
    dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
    dispatcher = get_dispatcher(dispatcher)

    bot.delete_webhook()
    url = urljoin(HOSTING_URL, TOKEN)
    bot.set_webhook(url=url)

    @app.route('/' + TOKEN, methods=['POST'])
    def webhook():
        json_string = request.stream.read().decode('utf-8')
        update = Update.de_json(json.loads(json_string), bot)
        dispatcher.process_update(update)
        return 'ok', 200


main()
# since this module is imported in wsgi, so __name__ is not  '__main__'
# if __name__ == '__main__':
#    main()
