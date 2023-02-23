import asyncio

from aiogram.types import Message
from aiogram.utils.exceptions import BadRequest, Unauthorized
from sqlalchemy import select, delete

from models import *


async def admin_handler(message: Message):
    async with message.bot.get('session')() as session:
        users = (await session.execute(select(User).filter_by(blocked=False))).scalars().all()

        for user in users:
            try:
                await message.send_copy(user.user_id)
                await asyncio.sleep(0.5)
            except (Unauthorized, BadRequest):
                await session.execute(delete(User).filter_by(user_id=user.user_id))
