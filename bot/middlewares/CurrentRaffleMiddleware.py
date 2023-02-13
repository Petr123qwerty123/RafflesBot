import datetime

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from sqlalchemy import select, and_, inspect, func
from models import *


class CurrentRaffleMiddleware(LifetimeControllerMiddleware):
    def __init__(self):
        super().__init__()

    async def pre_process(self, obj, data, *args):
        async with obj.bot.get('session')() as session:
            now = datetime.datetime.now()

            current_raffle = (
                await session.execute(
                    select(Raffle).
                    filter(
                        and_(
                            func.date(inspect(Raffle).c.start_datetime) <= now,
                            func.date(inspect(Raffle).c.end_datetime) >= now
                        )
                    )
                )
            ).scalar()

            if current_raffle:
                data['current_raffle']: Raffle = current_raffle
            else:
                data['current_raffle'] = None
