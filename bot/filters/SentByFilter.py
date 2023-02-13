import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery, ChatMemberUpdated
from aiogram.types.message import Message
from sqlalchemy import select

from models import *


class SentByFilter(BoundFilter):
    key = 'sent_by'

    def __init__(self, sent_by: str):
        self.sent_by = sent_by

    async def check(self, query: typing.Union[Message, CallbackQuery, ChatMemberUpdated]) -> typing.Union[User, Admin, bool, None]:
        async with query.bot.get('session')() as session:
            obj = (await session.execute(select(User).filter_by(user_id=query.from_user.id))).scalar() or \
                  (await session.execute(select(Admin).filter_by(user_id=query.from_user.id))).scalar()

            if obj:
                return {f'{type(obj).__name__}'.lower(): obj} if self.sent_by == type(obj).__name__ else False
            else:
                return self.sent_by == 'new'
