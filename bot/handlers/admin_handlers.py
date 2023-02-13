from aiogram.types import Message
from aiogram.utils.exceptions import BotBlocked
from sqlalchemy import select

from models import *


async def admin_handler(message: Message):
    async with message.bot.get('session')() as session:
        users = (await session.execute(select(User).filter_by(blocked=False))).scalars().all()

        for user in users:
            try:
                await message.send_copy(user.user_id)
            except BotBlocked:
                user.alive = False
                session.add(user)

        await session.commit()
