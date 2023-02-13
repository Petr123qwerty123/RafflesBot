from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class CheckSubscriptionsKeyboard(InlineKeyboardMarkup):
    def __init__(self):
        self.inline_keyboard = [
            [InlineKeyboardButton('Проверить подписки ✅', callback_data='check_subscriptions')]
        ]
        super().__init__(inline_keyboard=self.inline_keyboard)
