from typing import List, Tuple

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class EmojiCaptchaKeyboard(InlineKeyboardMarkup):
    def __init__(self, items: List[Tuple[str]]):
        self.keyboard_row = []

        for item in items:
            emoji = item[0]
            title = item[1]

            self.keyboard_row.append(InlineKeyboardButton(emoji, callback_data=f'emoji_captcha:{title}'))

        self.inline_keyboard = [self.keyboard_row]
        super().__init__(inline_keyboard=self.inline_keyboard)
