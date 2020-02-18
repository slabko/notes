import sqlalchemy as sa
import sqlalchemy.orm as orm
from .basemetadata import SqlAlchemyBase


__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file")

    connection_string = ''.join([
        '''sqlite:///''',
        db_file.strip(),
        '?check_same_thread=False'
    ])

    engine = sa.create_engine(connection_string, echo=False)

    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models  # noqa: F401
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> orm.Session:
    if __factory:
        return __factory()
    else:
        raise Exception('global_init must be called before create_session')
