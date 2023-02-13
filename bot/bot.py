from aiogram import Dispatcher
from aiogram.types import ChatType, ContentType

from .filters import *
from .handlers import *
from .states import *
from .middlewares import *


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(SentByFilter)
    dp.filters_factory.bind(CaptchaPassedFilter)
    dp.filters_factory.bind(UserActivityFilter)


def register_all_middlewares(dp: Dispatcher):
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(CurrentRaffleMiddleware())


def register_new_handlers(dp: Dispatcher):
    dp.register_message_handler(entry_handler,
                                chat_type=ChatType.PRIVATE,
                                sent_by='new',
                                state='*')
    dp.register_callback_query_handler(captcha_passed_callback_query_handler,
                                       chat_type=ChatType.PRIVATE,
                                       sent_by='new',
                                       captcha_passed=True,
                                       state=RaffleStates.emoji_captcha)
    dp.register_callback_query_handler(captcha_failed_callback_query_handler,
                                       chat_type=ChatType.PRIVATE,
                                       sent_by='new',
                                       captcha_passed=False,
                                       state=RaffleStates.emoji_captcha)


def register_user_handler(dp: Dispatcher):
    dp.register_message_handler(user_start_handler,
                                chat_type=ChatType.PRIVATE,
                                sent_by='User',
                                state=RaffleStates.checking_subscriptions)
    dp.register_callback_query_handler(check_subscriptions_callback_query_handler,
                                       chat_type=ChatType.PRIVATE,
                                       text='check_subscriptions',
                                       sent_by='User',
                                       state=RaffleStates.checking_subscriptions)
    dp.register_my_chat_member_handler(user_ban_bot_my_chat_member_handler,
                                       chat_type=ChatType.PRIVATE,
                                       sent_by='User',
                                       user_activity='banned_by_user',
                                       state='*')
    dp.register_my_chat_member_handler(user_unban_bot_my_chat_member_handler,
                                       chat_type=ChatType.PRIVATE,
                                       sent_by='User',
                                       user_activity='unbanned_by_user',
                                       state='*')
    dp.register_chat_member_handler(user_deleted_from_channel_chat_member_handler,
                                    chat_type=ChatType.CHANNEL,
                                    sent_by='User',
                                    user_activity='deleted_from_channel',
                                    state='*')


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_handler,
                                chat_type=ChatType.PRIVATE,
                                content_types=ContentType.all(),
                                sent_by='Admin',
                                state='*')


def register_all_handlers(dp: Dispatcher):
    register_new_handlers(dp)
    register_user_handler(dp)
    register_admin_handlers(dp)
