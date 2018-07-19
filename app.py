"""
user subscribes
save user telegram id, trakt credentials
ask for current timezone/location, notification delay or time

every ? hours check calendar if new episodes came up today and put them in queue with user specific delay/time
every 1 hour post stuff from queue

every week refresh tokens
"""
from core.settings import TELEGRAM_BOT_TOKEN  # should be loaded first
from client.bot import start_bot


def main():
    start_bot(TELEGRAM_BOT_TOKEN)


if __name__ == '__main__':
    main()
