import logging

from telegram import Bot, Update, User as TeleUser
from telegram.ext import CommandHandler, Updater

from core.db import Session
from core.settings import TELEGRAM_BOT_TOKEN
from .models import User


def start_command(bot: Bot, update: Update):
    bot.send_message(update.message.chat.id, "Howdy, how are you doing?")


def subscribe(bot: Bot, update: Update):
    s = Session()
    teleuser = update.effective_user  # type: TeleUser
    user = User(telegram_id=teleuser.id,
                first_name=teleuser.first_name, last_name=teleuser.last_name,
                username=teleuser.username)

    # s.add(user)
    # s.commit()

    if not s.query(User).filter(User.telegram_id == teleuser.id).one_or_none():
        s.add(user)
        s.commit()
        bot.send_message(update.effective_chat.id, 'ok')
    else:
        bot.send_message(update.effective_chat.id, 'already')
    s.close()


def get_self(bot: Bot, update: Update):
    s = Session()
    teleuser = update.effective_user  # type: TeleUser
    user = s.query(User).filter(User.telegram_id == teleuser.id).one_or_none()
    if not user:
        bot.send_message(update.effective_chat.id, 'not subscribed')
        return
    msg = '> ' + user.name + ' ~ ' + str(user.trakt)
    bot.send_message(update.effective_chat.id, msg)
    s.close()


def error_callback(bot: Bot, update: Update, error):
    print(error)


def start_bot(token=None):
    if not token:
        token = TELEGRAM_BOT_TOKEN
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

    updater = Updater(token=token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('sub', subscribe))
    dp.add_handler(CommandHandler('get', get_self))
    dp.add_error_handler(error_callback)
    print('start')
    updater.start_polling()
    updater.idle()
