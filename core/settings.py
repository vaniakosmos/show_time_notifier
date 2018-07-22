import logging.config
import multiprocessing
from os.path import dirname

import easy_env
from dotenv import find_dotenv, load_dotenv

from core.utils import load_modules


load_dotenv(find_dotenv())

# env and consts
BASE_DIR = dirname(dirname(__file__))
DEBUG = easy_env.get_bool('DEBUG', False)
DATABASE_URL = easy_env.get_str('DATABASE_URL', raise_error=True)

# telegram
TELEGRAM_BOT_TOKEN = easy_env.get_str('TELEGRAM_BOT_TOKEN')

# trakt
TRAKT_CLIENT_ID = easy_env.get_str('TRAKT_CLIENT_ID')
TRAKT_CLIENT_SECRET = easy_env.get_str('TRAKT_CLIENT_SECRET')
TRAKT_REDIRECT_URI = easy_env.get_str('TRAKT_REDIRECT_URI')

# celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_WORKER_CONCURRENCY = easy_env.get_int('CELERY_WORKER_CONCURRENCY',
                                             multiprocessing.cpu_count())

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

load_modules('models', BASE_DIR)
