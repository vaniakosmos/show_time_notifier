from typing import Optional, Union

import requests
from apistar import Route, http

from core.db import session_scope
from core.models import State, User
from .models import TraktCred
from .utils import params_for_token, turl


def check_state(state) -> Optional[int]:
    """
    check if this state in db
    return associated with state telegram_id
    delete state from db
    """
    with session_scope() as s:
        state = s.query(State).filter(State.state == state).one_or_none()
        if state:
            s.delete(state)
            return state.telegram_id


def save_credentials(telegram_id, data: dict):
    with session_scope() as s:
        user = s.query(User).filter(User.telegram_id == telegram_id).one()
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        cred = TraktCred(user_id=user.id, access_token=access_token, refresh_token=refresh_token)
        s.add(cred)


def fetch_auth_code(code: str = None, state: str = None) -> Union[str, http.Response]:
    if not code:
        return "no is no\nbut it's fine, i understand\nmaybe next time (:"

    telegram_id = check_state(state)
    if not telegram_id:
        return http.Response("wow, this is very bad state in ur url. don't do that again",
                             status_code=400)
    url = turl('oauth/token')
    res = requests.post(url, json=params_for_token(code=code))
    data = res.json()
    save_credentials(telegram_id, data)
    return 'everything is fine, my dude, u may close this tab now and jump back to the bot'


trakt_routes = [
    Route('/auth/', method='GET', handler=fetch_auth_code),
]
