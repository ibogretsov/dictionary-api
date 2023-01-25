import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Word(Base):

    __tablename__ = 'word'

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    word = sa.Column(sa.String(length=256), index=True)
    examples = sa.Column(postgresql.ARRAY(sa.Text))
    translations = sa.Column(postgresql.JSON(none_as_null=True))
    definitions = sa.Column(postgresql.JSON(none_as_null=True))
