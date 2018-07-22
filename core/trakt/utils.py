from urllib.parse import urlencode

from core.settings import TRAKT_CLIENT_ID, TRAKT_CLIENT_SECRET, TRAKT_REDIRECT_URI


def build_url(*args):
    return '/'.join(map(str, args))


def api_url(*args):
    return build_url('https://api.trakt.tv', *args)


def site_url(*args):
    return build_url('https://trakt.tv', *args)


def build_auth_url(state):
    return api_url('oauth/authorize') + '?' + urlencode({
        'response_type': 'code',
        'client_id': TRAKT_CLIENT_ID,
        'redirect_uri': TRAKT_REDIRECT_URI,
        'state': state,
    })


def params_for_token(code=None, refresh_token=None):
    if code:
        return {
            "code": code,
            "client_id": TRAKT_CLIENT_ID,
            "client_secret": TRAKT_CLIENT_SECRET,
            "redirect_uri": TRAKT_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
    elif refresh_token:
        return {
            "refresh_token": refresh_token,
            "client_id": TRAKT_CLIENT_ID,
            "client_secret": TRAKT_CLIENT_SECRET,
            "redirect_uri": TRAKT_REDIRECT_URI,
            "grant_type": "refresh_token",
        }
    raise ValueError('Code or refresh_token should be specified.')
