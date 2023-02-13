import typing

from aiogram.types import Message, CallbackQuery, ParseMode, ChatMemberUpdated
from sqlalchemy import delete, select

from models import *
from ..keyboards import *


async def user_start_handler(message: Message,
                             user: User,
                             current_raffle: typing.Optional[Raffle]):
    async with message.bot.get('session')() as session:
        await message.answer(f'Привет, {message.from_user.full_name}!')

        if current_raffle:
            participant = (await session.execute(select(Participant).filter_by(user=user,
                                                                               raffle=current_raffle))).scalar()

            if participant:
                keyboard = None
            else:
                keyboard = CheckSubscriptionsKeyboard()

            if current_raffle.image_url:
                await message.answer_photo(current_raffle.image_url,
                                           reply_markup=keyboard,
                                           caption=current_raffle.full_description,
                                           parse_mode=ParseMode.HTML)
            else:
                await message.answer(current_raffle.full_description,
                                     reply_markup=keyboard,
                                     parse_mode=ParseMode.HTML)
        else:
            await message.answer('На данный момент не проходит ни один розыгрыш(')


async def register_new_participant(callback_query: CallbackQuery,
                                   user: User,
                                   current_raffle: typing.Optional[Raffle]):
    async with callback_query.bot.get('session')() as session:
        new_participant = Participant(user=user,
                                      raffle=current_raffle)
        session.add(new_participant)
        await session.commit()


async def check_user_subscriptions(query: typing.Union[CallbackQuery, ChatMemberUpdated],
                                   user: User,
                                   current_raffle: typing.Optional[Raffle]):
    return all(
        [
            (
                await query.bot.get_chat_member(
                    channel.channel_id,
                    user.user_id
                )
            ).status in ('creator',
                         'owner',
                         'administrator',
                         'member')
            for channel in current_raffle.channels]
    )


async def check_subscriptions_callback_query_handler(callback_query: CallbackQuery,
                                                     user: User,
                                                     current_raffle: typing.Optional[Raffle]):
    if current_raffle:
        check_result = await check_user_subscriptions(callback_query, user, current_raffle)
        if check_result:
            await callback_query.message.answer('<b>Поздравляем, вы выполнили все условия конкурса 🥳</b>',
                                                parse_mode=ParseMode.HTML)
            await register_new_participant(callback_query,
                                           user,
                                           current_raffle)
            await callback_query.message.delete()
        else:
            await callback_query.message.answer('⚠ Условия не выполнены !\n\n'
                                                'Возможно вы не подписались на один из каналов👆\n\n'
                                                'Либо кто-то из админов ещё не принял вашу заявку '
                                                '(заявки принимают вручную, дабы избежать наплыва ботов)')
    else:
        await callback_query.message.answer('На данный момент не проходит ни один розыгрыш(')


async def user_ban_bot_my_chat_member_handler(event: ChatMemberUpdated, user: User):
    async with event.bot.get('session')() as session:
        user.alive = False
        session.add(user)
        await session.commit()


async def user_unban_bot_my_chat_member_handler(event: ChatMemberUpdated, user: User):
    async with event.bot.get('session')() as session:
        user.alive = True
        session.add(user)
        await session.commit()


async def user_deleted_from_channel_chat_member_handler(event: ChatMemberUpdated,
                                                        user: User,
                                                        current_raffle: typing.Optional[Raffle]):
    async with event.bot.get('session')() as session:
        check_result = await check_user_subscriptions(event, user, current_raffle)

        if not check_result:
            await session.execute(delete(Participant).filter_by(user=user, raffle=current_raffle))

            channel = (await session.execute(select(Channel).filter_by(channel_id=event.chat.id))).scalar()

            if user.alive:
                keyboard = CheckSubscriptionsKeyboard()

                await event.bot.send_message(user.user_id,
                                             'Вы были исключены из участников розыгрыша, потому что '
                                             f'отписались от <a href="{channel.link}">{channel.title}</a> '
                                             'раньше срока его завершения!',
                                             reply_markup=keyboard,
                                             parse_mode=ParseMode.HTML,
                                             disable_web_page_preview=True)

            await session.commit()
