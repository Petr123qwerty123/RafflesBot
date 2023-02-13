import datetime
import typing

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ParseMode, CallbackQuery

from models import *
from ..keyboards import *
from ..modules.captcha import emoji_captcha
from ..states.RaffleStates import RaffleStates


async def entry_handler(obj: typing.Union[Message, CallbackQuery], state: FSMContext):
    items, correct_title = emoji_captcha.generate()

    await state.update_data(captcha_correct_answer=correct_title)

    text = f'Для прохождения каптчи нажмите на кнопку, где изображено: <b>{correct_title}</b>'
    keyboard = EmojiCaptchaKeyboard(items)

    if isinstance(obj, Message):
        await obj.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    elif isinstance(obj, CallbackQuery):
        await obj.message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)

    await RaffleStates.emoji_captcha.set()


async def register_new_user(callback_query: CallbackQuery):
    async with callback_query.bot.get('session')() as session:
        new_user = User(first_name=callback_query.from_user.first_name,
                        registration_datetime=datetime.datetime.now(),
                        username=callback_query.from_user.username,
                        last_name=callback_query.from_user.last_name)

        new_user.user_id = callback_query.from_user.id

        session.add(new_user)
        await session.commit()


async def captcha_passed_callback_query_handler(callback_query: CallbackQuery, current_raffle: typing.Optional[Raffle]):
    await callback_query.message.delete()

    await register_new_user(callback_query)

    await callback_query.message.answer(f'Привет, {callback_query.from_user.full_name}!')

    if current_raffle:
        keyboard = CheckSubscriptionsKeyboard()

        if current_raffle.image_url:
            await callback_query.message.answer_photo(current_raffle.image_url,
                                                      reply_markup=keyboard,
                                                      caption=current_raffle.full_description,
                                                      parse_mode=ParseMode.HTML)
        else:
            await callback_query.message.answer(current_raffle.full_description,
                                                reply_markup=keyboard,
                                                parse_mode=ParseMode.HTML)
    else:
        await callback_query.message.answer('На данный момент не проходит ни один розыгрыш(')

    await RaffleStates.checking_subscriptions.set()


async def captcha_failed_callback_query_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await entry_handler(callback_query, state)
