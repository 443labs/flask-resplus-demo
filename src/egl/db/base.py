from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session

from egl.db.sessions import db

DBSession = scoped_session(db.session)


class _Base(object):
    query = DBSession.query_property()


Base = declarative_base(cls=_Base)
