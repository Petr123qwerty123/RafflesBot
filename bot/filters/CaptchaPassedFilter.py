from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery


class CaptchaPassedFilter(BoundFilter):
    key = 'captcha_passed'

    def __init__(self, dispatcher, captcha_passed: bool):
        self.dispatcher = dispatcher
        self.captcha_passed = captcha_passed

    async def check(self, callback_query: CallbackQuery) -> bool:
        state = self.dispatcher.current_state()

        cache = await state.get_data()

        captcha_correct_answer = cache.get('captcha_correct_answer')
        captcha_user_answer = callback_query.data.split(':')[1]

        return self.captcha_passed == (captcha_correct_answer == captcha_user_answer)
