from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from core.db import Model


class TraktCred(Model):
    __tablename__ = 'trakt_creds'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"),
                     unique=True, nullable=False)
    user = relationship("User", backref=backref(
        "trakt", uselist=False, cascade="all, delete-orphan"))
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
