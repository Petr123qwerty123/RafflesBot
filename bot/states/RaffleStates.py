from aiogram.dispatcher.filters.state import StatesGroup, State


class RaffleStates(StatesGroup):
    emoji_captcha = State()
    checking_subscriptions = State()
