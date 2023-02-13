from sqlalchemy import MetaData, Table
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import mapper, relationship, sessionmaker

from config import config

from models import *

__engine = create_async_engine(config['POSTGRES_DB']['postgres_uri'], echo=False)
__metadata = MetaData()


async def init_db():
    async with __engine.connect() as conn:
        await conn.run_sync(
            __metadata.reflect,
            only=[
                'admins',
                'channels',
                'participants',
                'raffles',
                'raffles_channels',
                'users'
            ]
        )

    __admins_table = Table('admins',
                           __metadata,
                           autoload_with=__engine)
    __channels_table = Table('channels',
                             __metadata,
                             autoload_with=__engine)
    __participants_table = Table('participants',
                                 __metadata,
                                 autoload_with=__engine)
    __raffles_table = Table('raffles',
                            __metadata,
                            autoload_with=__engine)
    __raffles_channels_table = Table('raffles_channels',
                                     __metadata,
                                     autoload_with=__engine)
    __users_table = Table('users',
                          __metadata,
                          autoload_with=__engine)

    mapper(Channel,
           __channels_table)
    mapper(User,
           __users_table,
           polymorphic_on=__users_table.c.role_id,
           polymorphic_identity=1)
    mapper(Admin,
           __admins_table,
           polymorphic_on=__users_table.c.role_id,
           polymorphic_identity=2,
           inherits=User)
    mapper(Participant,
           __participants_table,
           properties={
               'user': relationship(User, lazy='selectin'),
               'raffle': relationship(Raffle, back_populates='participants', lazy='selectin')
           })
    mapper(Raffle,
           __raffles_table,
           properties={
               'channels': relationship(Channel, secondary=__raffles_channels_table, lazy='selectin'),
               'participants': relationship(Participant, back_populates='raffle', lazy='selectin')
           })

    db = sessionmaker(bind=__engine, expire_on_commit=False, class_=AsyncSession)

    return db
