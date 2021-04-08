import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Base

class Reporter(object):
    def login(self, dsn):
        raise Exception("please overwrite me")

    def report(self, row_obj):
        raise Exception("please overwrite me")

class DBReport(Reporter):
    def login(self, dsn):
        self._db_session = None
        engine = create_engine(
            dsn,
            json_serializer = lambda obj: json.dumps(obj, ensure_ascii=False),
            connect_args = {"connect_timeout": 10},
        )
        Base.metadata.create_all(engine)
        self._db_session = sessionmaker(engine)()

    def report(self, row_obj):
        if self._db_session is None:
            raise Exception("the db session is nil")
        self._db_session.add(row_obj)
        self._db_session.commit()