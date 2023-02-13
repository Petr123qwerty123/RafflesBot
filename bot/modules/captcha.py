import random


class EmojiCaptcha:
    emoji = {
        '🍎': 'Яблоко',
        '🫐': 'Черника',
        '🍋': 'Лимон',
        '🍍': 'Ананас',
        '🍇': 'Виноград',
        '🥥': 'Кокос',
        '🍐': 'Груша',
        '🍑': 'Персик',
        '🥝': 'Киви',
        '🍒': 'Вишня',
        '🍓': 'Клубника',
        '🍊': 'Мандарин',
        '🍉': 'Арбуз'
    }

    def generate(self, length: int = 3):
        items = random.sample(list(self.emoji.items()), length)

        correct_item = random.choice(items)
        correct_title = correct_item[1]

        return items, correct_title


emoji_captcha = EmojiCaptcha()
