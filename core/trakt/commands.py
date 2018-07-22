import logging
from typing import Tuple

from sqlalchemy.orm import Session
from telegram import Bot, Update, User as TeleUser

from core.db import session_wrapper
from core.models import User, make_state
from .tasks import fetch_calendars, publish_user_calendar
from .models import TraktCred
from .utils import build_auth_url


logger = logging.getLogger(__name__)


def create_user(session: Session, teleuser: TeleUser) -> Tuple[User, bool]:
    user = session.query(User).filter(User.telegram_id == teleuser.id).one_or_none()
    if not user:
        user = User(telegram_id=teleuser.id,
                    first_name=teleuser.first_name,
                    last_name=teleuser.last_name,
                    username=teleuser.username)
        session.add(user)
        logger.debug(f'user {user.name} created')
        return user, True
    return user, False


@session_wrapper
def subscribe(bot: Bot, update: Update, session: Session):
    teleuser = update.effective_user  # type: TeleUser
    user, created = create_user(session, teleuser)
    if not created and user.trakt:
        msg = f"already subscribed to trakt"
        bot.send_message(update.effective_chat.id, msg)
        return
    state = make_state(session, teleuser.id)
    auth_url = build_auth_url(state)
    msg = f"hear is your auth link, pal\n{auth_url}"
    bot.send_message(update.effective_chat.id, msg, disable_web_page_preview=True)


@session_wrapper
def unsubscribe(bot: Bot, update: Update, session: Session):
    teleuser = update.effective_user  # type: TeleUser
    cred = session.query(TraktCred).join(User) \
        .filter(User.telegram_id == teleuser.id) \
        .one_or_none()
    if cred:
        session.delete(cred)
        bot.send_message(teleuser.id, 'unsubscribed from trakt')
    else:
        bot.send_message(teleuser.id, "wasn't subscribed to trakt")


@session_wrapper
def fetch_today(bot: Bot, update: Update, session: Session):
    fetch_calendars()


def update_urls(bot: Bot, update: Update):
    """todo: update watch/download urls"""


def notify(bot: Bot, user: User):
    reply_markup = None  # url
    msg = 'notify!'
    bot.send_message(user.telegram_id, msg, reply_markup=reply_markup)


def repost_calendar(bot: Bot, update: Update, args):
    """todo: repost episodes from last N days"""
