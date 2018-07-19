import logging

from telegram import Bot, Update, User as TeleUser
from telegram.ext import CommandHandler, Updater

import core.trakt.commands as trakt
from core.db import session_scope
from core.settings import TELEGRAM_BOT_TOKEN
from .models import User


logger = logging.getLogger(__name__)


def start_command(bot: Bot, update: Update):
    bot.send_message(update.message.chat.id, "foo bar start command")


def get_self(bot: Bot, update: Update):
    with session_scope() as s:
        teleuser = update.effective_user  # type: TeleUser
        user = s.query(User).filter(User.telegram_id == teleuser.id).one_or_none()
        if not user:
            bot.send_message(update.effective_chat.id, 'never subscribed to anything')
            return
        msg = ''
        msg += '✅ trakt' if user.trakt else '🚫 trakt'
        bot.send_message(update.effective_chat.id, msg)


def error_callback(bot: Bot, update: Update, error):
    logger.exception(error)


def start_bot(token=None):
    if not token:
        token = TELEGRAM_BOT_TOKEN
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

    updater = Updater(token=token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('sub_trakt', trakt.subscribe))
    dp.add_handler(CommandHandler('unsub_trakt', trakt.unsubscribe))
    dp.add_handler(CommandHandler('get', get_self))
    dp.add_error_handler(error_callback)
    logger.info('= ' * 33)
    logger.info('| STARTING BOT')
    logger.info('= ' * 33)
    updater.start_polling()
    updater.idle()
