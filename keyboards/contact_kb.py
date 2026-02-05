from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def request_contact_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить свой контакт", request_contact=True)],
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Нажмите кнопку или введите номер"
    )
