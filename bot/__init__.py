import inspect
import logging.config
import logging
import os
from contextlib import contextmanager

import telegram
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from telegram.ext import Updater, Handler

config_path = os.path.abspath(os.path.join(os.getcwd(), 'cfg', 'config.yml'))
logger = logging.getLogger('mkbot')
os.makedirs(os.path.join(os.getcwd(), 'Logs'), exist_ok=True)

try:
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        logging.config.dictConfig(config['logging'])
        logger.info('Configuration loaded from file "%s"', config_path)

except FileNotFoundError as e:
    raise e


@contextmanager
def session_context():
    try:
        yield session
    finally:
        session.remove()


engine = create_engine('sqlite:///database.db', echo=False)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)


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


def custom_handler(self, *args, **kwargs):
    try:
        ret = self._handle_update(*args, **kwargs)
    finally:
        session.remove()
    return ret


Handler._handle_update = Handler.handle_update
Handler.handle_update = custom_handler

