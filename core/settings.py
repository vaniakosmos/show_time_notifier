import logging
from os.path import dirname

import easy_env
from dotenv import find_dotenv, load_dotenv

from core.utils import load_models


load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)

# env and consts
BASE_DIR = dirname(dirname(__file__))
DEBUG = easy_env.get_bool('DEBUG', False)
DATABASE_URL = easy_env.get_str('DATABASE_URL', raise_error=True)

TELEGRAM_BOT_TOKEN = easy_env.get_str('TELEGRAM_BOT_TOKEN')

TRAKT_CLIENT_ID = easy_env.get_str('TRAKT_CLIENT_ID')
TRAKT_CLIENT_SECRET = easy_env.get_str('TRAKT_CLIENT_SECRET')
TRAKT_REDIRECT_URI = easy_env.get_str('TRAKT_REDIRECT_URI')

# logging
# todo: setup properly
logging.basicConfig(level=10 if DEBUG else 20)

# models
load_models(BASE_DIR, logger)
