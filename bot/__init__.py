import os

import yaml
from telegram import Bot
from telegram.ext import Updater

config_path = os.path.abspath(os.path.join(os.getcwd(), 'cfg', 'config.yml'))

try:
    with open(config_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as e:
    raise e

updater = Updater(token=config['telegram']['token'], use_context=True)
bot = Bot(token=config['telegram']['token'])
dispatcher = updater.dispatcher
jobs = updater.job_queue
