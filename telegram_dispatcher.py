import logging
import traceback
import urllib.parse
import re
from uuid import uuid4
from index import search_command

from pylatexenc.latex2text import LatexNodes2Text
from telegram import (InlineQueryResultArticle, InlineQueryResultGif,
                      InputTextMessageContent, ParseMode, Update)
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, InlineQueryHandler)
from telegram.utils.helpers import escape_markdown

# ------- Loggging-----------
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# --- telegram commands handlers ---

def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(r'This is very simple inline bot. Try typing "@Latex_reader_bot \alpha" in any chat')

def inlinequery(update: Update, _: CallbackContext) -> None:
    """Handle the inline query."""
    try:
        query = update.inline_query.query
        if (query == ""):
            return

        logger.info(f'Inline query {update.effective_user.name} ' + query)
        url = r'https://latex.codecogs.com/gif.latex?\dpi{300}&space;\huge&space;' + \
            urllib.parse.quote(query)
        url2 = r'https://latex.codecogs.com/png.latex?\inline&space;\dpi{150}&space;\bg_white&space;' + \
            urllib.parse.quote(query)
        
        last_word = re.findall(r'\\(\w*)$', query)
        suggest=''
        if (last_word):
            commands = search_command(last_word[-1], 5)
            suggest = ' '.join(commands)

        simple = LatexNodes2Text().latex_to_text(query)
        text = f"{escape_markdown(query)}\n {escape_markdown(simple)}\n [.]({url})"
        results = [
            InlineQueryResultArticle(
                id=uuid4(),
                title = query,
                input_message_content=InputTextMessageContent(text, parse_mode=ParseMode.MARKDOWN),
                thumb_url = url2,
                description=simple + '\n' + suggest,
            ),
        ]
        update.inline_query.answer(results, cache_time = 0) #Tellegram cache is case insencitive
    except Exception as error:
        logger.error(traceback.format_exc())

def get_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    return dispatcher
