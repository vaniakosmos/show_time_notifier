"""
user subscribes
save user telegram id, trakt credentials
ask for current timezone/location, notification delay or time

every ? hours check calendar if new episodes came up today and put them in queue with user specific delay/time
every 1 hour post stuff from queue

every week refresh tokens
"""
import argparse

from core.settings import TELEGRAM_BOT_TOKEN  # should be loaded first


if __name__ == '__main__':
    from core.app import start_app
    from core.bot import start_bot

    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    args = parser.parse_args()
    if args.command == 'app':
        start_app()
    elif args.command == 'bot':
        start_bot(TELEGRAM_BOT_TOKEN)
    else:
        raise ValueError('Invalid command')
