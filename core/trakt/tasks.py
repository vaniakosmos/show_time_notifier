import logging
from collections import namedtuple
from datetime import datetime, timedelta

import requests
from celery.schedules import crontab
from sqlalchemy.orm import Session
from telegram import Bot, ParseMode

from core import settings
from core.celery import app
from core.db import session_wrapper
from core.models import User
from core.trakt.models import TraktCred
from .utils import api_url, site_url


logger = logging.getLogger(__name__)

Show = namedtuple('Show', 'title year slug')
Episode = namedtuple('Episode', 'season number title id')


def make_calendar_url(offset=7, days=1):
    """calendars/my/shows/start_date/days"""
    start_data = datetime.now() - timedelta(days=offset)
    start_date_str = start_data.strftime('%Y-%m-%d')
    url = api_url('calendars/my/shows', start_date_str, days)
    return url


def publish_user_calendar(bot: Bot, user: User, days: int):
    url = make_calendar_url(days=days)
    access_token = user.trakt.access_token
    res = requests.get(url, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'trakt-api-version': '2',
        'trakt-api-key': settings.TRAKT_CLIENT_ID,
    })
    episodes = res.json()[::-1]
    publish(bot, user.telegram_id, episodes)


def deserialize(data: dict):
    episode_dict = data['episode']
    episode = Episode(
        id=episode_dict['ids']['trakt'],
        title=episode_dict['title'],
        season=episode_dict['season'],
        number=episode_dict['number'],
    )
    show_dict = data['show']
    show = Show(
        title=show_dict['title'],
        slug=show_dict['ids']['slug'],
        year=show_dict['year'],
    )
    return show, episode


def pad_zero(num: int):
    # return str(num).rjust(2, '0')
    return str(num)


def publish(bot: Bot, chat_id, chunks: list):
    for chunk in chunks:
        show, episode = deserialize(chunk)

        episode_url = site_url('shows', show.slug, 'seasons',
                               episode.season, 'episodes', episode.number)
        season_url = site_url('shows', show.slug, 'seasons', episode.season)
        s, n = pad_zero(episode.season), pad_zero(episode.number)
        lines = [
            f'**{show.title}**',
            f'[Season {s}]({season_url}), [Episode {n}: {episode.title}]({episode_url})',
        ]
        msg = '\n'.join(lines)
        bot.send_message(chat_id, msg, parse_mode=ParseMode.MARKDOWN)


@app.task
@session_wrapper
def fetch_calendars(session: Session=None):
    bot = Bot(settings.TELEGRAM_BOT_TOKEN)
    users = session.query(User).join(TraktCred).all()
    for user in users:
        publish_user_calendar(bot, user, days=1)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **_):
    logger.info('SCHEDULING TRAKT')
    cron = crontab(hour='*', minute='1')
    sender.add_periodic_task(cron, fetch_calendars.s(), name='trakt.fetch_calendars')
