import inspect
import logging.config
import logging
import os

import telegram
import yaml
from telegram.ext import Updater

config_path = os.path.abspath(os.path.join(os.getcwd(), 'cfg', 'config.yml'))
logger = logging.getLogger('mkbot')

try:
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        logging.config.dictConfig(config['logging'])
        logger.info('Configuration loaded from file "%s"', config_path)

except FileNotFoundError as e:
    raise e


class MyBot(telegram.Bot):
    def __init__(self, token):
        super().__init__(token)

    def send_message(self, chat_id, text, *args, **kwargs):
        caller = inspect.getouterframes(inspect.currentframe(), 1)[1]
        try:
            super().send_message(chat_id, text, *args, **kwargs)
            logger.debug('[SEND_MESSAGE] Successfully sent from {} function={}'
                         ' to user={}'.format(caller.filename, caller.function, chat_id))
        except telegram.error.TelegramError as e:
            logger.error('[SEND_MESSAGE] Failed sent from {} function={}'
                         ' to user={}'.format(caller.filename, caller.function, chat_id))

    def send_photo(self, chat_id, photo, *args, **kwargs):
        caller = inspect.getouterframes(inspect.currentframe(), 1)[1]
        try:
            super().send_photo(chat_id, photo, *args, **kwargs)
            logger.debug('[SEND_PHOTO] Successfully sent from {} function={}'
                         ' to user={}'.format(caller.filename, caller.function, chat_id))
        except telegram.error.TelegramError as e:
            logger.error('[SEND_PHOTO] Failed sent from {} function={}'
                         ' to user={}'.format(caller.filename, caller.function, chat_id))

    def edit_message_media(self, *args, **kwargs):
        caller = inspect.getouterframes(inspect.currentframe(), 1)[1]
        try:
            super().edit_message_media(*args, **kwargs)
            logger.debug('[EDIT_MESSAGE] Successfully edit message from {} function={}'
                         ' to user={}'.format(caller.filename, caller.function,
                                               kwargs.get('chat_id')))
        except telegram.error.TelegramError as e:
            logger.debug('[EDIT_MESSAGE] Failed edit message from {} function={}'
                         ' to user={}'.format(caller.filename, caller.function,
                                              kwargs.get('chat_id')))

    def send_document(self, chat_id, document, *args, **kwargs):
        caller = inspect.getouterframes(inspect.currentframe(), 1)[1]
        try:
            super().send_document(chat_id, document, *args, **kwargs)
            logger.debug('[SEND_DOCUMENT] Successfully sent from {} function={}'
                         ' to user={}'.format(caller.filename, caller.function, chat_id))
        except telegram.error.TelegramError as e:
            logger.debug('[SEND_DOCUMENT] Failed sent from {} function={}'
                         ' to user={}'.format(caller.filename, caller.function, chat_id))


updater = Updater(token=config['telegram']['token'], use_context=True)
bot = MyBot(token=config['telegram']['token'])
dispatcher = updater.dispatcher
jobs = updater.job_queue
