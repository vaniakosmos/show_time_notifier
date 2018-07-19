import uuid
from datetime import datetime

import sqlalchemy as sa

from core.db import Model, Session


class User(Model):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    telegram_id = sa.Column(sa.BigInteger, unique=True, nullable=False)
    first_name = sa.Column(sa.String, nullable=True)
    last_name = sa.Column(sa.String, nullable=True)
    username = sa.Column(sa.String, nullable=True)

    @property
    def name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        if self.first_name:
            return self.first_name
        if self.last_name:
            return self.last_name
        return self.username


class State(Model):
    __tablename__ = 'states'

    id = sa.Column(sa.Integer, primary_key=True)
    telegram_id = sa.Column(sa.BigInteger, nullable=False)
    state = sa.Column(sa.Text, nullable=False, index=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)


def make_state(session: Session, telegram_id):
    state_str = str(uuid.uuid4())
    state = State(telegram_id=telegram_id, state=state_str)
    session.add(state)
    return state_str
