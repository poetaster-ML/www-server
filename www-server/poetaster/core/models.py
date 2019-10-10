from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Integer, PrimaryKeyConstraint, String
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils import observes
from .columns import SlugColumn


def onupdate_version_increment(context):
    return 0


def relationship_ordered_by_version(argument, **kwargs):
    order_by = argument.version
    return relationship(
        argument, order_by=order_by, **kwargs)


class Versioned:
    version = Column(
        Integer,
        default=0,
        onupdate=onupdate_version_increment
    )


class Slugged:
    slug = SlugColumn()


class IDVersioned(Versioned):
    id = Column(Integer, autoincrement=True)

    @declared_attr
    def __table_args__(cls):
        return (
            PrimaryKeyConstraint(
                "id", "version",
            ),
        )


class SlugVersioned(Slugged, Versioned):
    @declared_attr
    def __table_args__(cls):
        return (
            PrimaryKeyConstraint(
                "slug", "version",
            ),
        )
