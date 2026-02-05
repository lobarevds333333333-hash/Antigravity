from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from lexicon.lexicon_ru import LEXICON_RU

def get_main_menu() -> ReplyKeyboardMarkup:
    btn_about = KeyboardButton(text=LEXICON_RU['about_btn'])
    btn_services = KeyboardButton(text=LEXICON_RU['services_btn'])
    btn_reviews = KeyboardButton(text=LEXICON_RU['reviews_btn'])
    btn_contacts = KeyboardButton(text=LEXICON_RU['contacts_btn'])
    btn_consult = KeyboardButton(text=LEXICON_RU['consultation_btn'])

    keyboard = [
        [btn_about, btn_services],
        [btn_reviews, btn_contacts],
        [btn_consult]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder='Выберите пункт меню...'
    )
