import asyncio

from config import config

from aiogram.contrib.fsm_storage.mongo import MongoStorage

from aiogram import Bot

from database import init_db

from bot import *


async def run():
    db = await init_db()

    bot_obj = Bot(token=config['BOT']['bot_token'])
    bot_obj['session'] = db

    storage = MongoStorage(uri=config['MONGO_DB']['mongo_uri'],
                           db_name=config['MONGO_DB']['mongo_db_name'])

    dp = Dispatcher(bot_obj, storage=storage)

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    print('Бот запущен...')

    await dp.start_polling(allowed_updates=['message',
                                            'callback_query',
                                            'inline_query',
                                            'my_chat_member',
                                            'chat_member'])


if __name__ == '__main__':
    asyncio.run(run())
