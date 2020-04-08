from django.core.management.base import BaseCommand as BaseDjangoCommand

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class BaseCommand(BaseDjangoCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        engine = create_engine('postgresql://postgres@db:5432/postgres')
        self.session = scoped_session(sessionmaker(
            bind=engine, expire_on_commit=False))
