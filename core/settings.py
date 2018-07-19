import logging
import logging.config
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
logging.addLevelName(logging.DEBUG, '🐛 ')
logging.addLevelName(logging.INFO, '📄️ ')
logging.addLevelName(logging.WARNING, '⚠️ ')
logging.addLevelName(logging.ERROR, '🚨 ')
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)20s:%(lineno)-4d  ⏩  %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO' if DEBUG else 'WARNING',
        'propagate': False,
    },
})

# models
load_models(BASE_DIR, logger)
