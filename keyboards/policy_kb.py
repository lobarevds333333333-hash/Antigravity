from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_policy_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Принять", callback_data="policy_accept")],
            [InlineKeyboardButton(text="❌ Отказать", callback_data="policy_decline")],
            [InlineKeyboardButton(text="📜 Читать Политику", url="https://disk.yandex.ru/i/rI3-2Cx2c2-UNA")]
        ]
    )
