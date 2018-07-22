import logging

from telegram import Bot, Update, User as TeleUser
from telegram.ext import CommandHandler, Updater

import core.trakt.commands as trakt
from core.db import Session, session_wrapper
from core.settings import TELEGRAM_BOT_TOKEN
from .models import User


logger = logging.getLogger(__name__)


def start_command(bot: Bot, update: Update):
    bot.send_message(update.message.chat.id, "foo bar start command")


@session_wrapper
def get_self(bot: Bot, update: Update, session: Session):
    teleuser = update.effective_user  # type: TeleUser
    user = session.query(User).filter(User.telegram_id == teleuser.id).one_or_none()
    if not user:
        bot.send_message(update.effective_chat.id, 'never subscribed to anything')
        return
    lines = [
        'subscriptions:',
        '✅ trakt' if user.trakt else '🚫 trakt',
    ]
    bot.send_message(update.effective_chat.id, '\n'.join(lines))


def error_callback(bot: Bot, update: Update, error):
    logger.exception(error)


def subscribe(bot: Bot, update: Update, args):
    if len(args) != 1:
        return
    service = args[0]
    if service == 'trakt':
        return trakt.subscribe(bot, update)


def unsubscribe(bot: Bot, update: Update, args):
    if len(args) != 1:
        return
    service = args[0]
    if service == 'trakt':
        return trakt.unsubscribe(bot, update)


def start_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('sub', subscribe, pass_args=True))
    dp.add_handler(CommandHandler('unsub', unsubscribe, pass_args=True))
    dp.add_handler(CommandHandler('check', trakt.fetch_today))
    dp.add_handler(CommandHandler('get', get_self))
    dp.add_error_handler(error_callback)
    logger.info('= ' * 33)
    logger.info('| STARTING BOT')
    logger.info('= ' * 33)
    updater.start_polling()
    # updater.idle()
