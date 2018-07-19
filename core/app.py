from apistar import App, Include

from core.settings import DEBUG
from .trakt.views import trakt_routes


routes = [
    Include('/trakt', name='trakt', routes=trakt_routes)
]

app = App(routes=routes)


def start_app():
    app.serve('0.0.0.0', 5000, debug=DEBUG)


if __name__ == '__main__':
    start_app()
