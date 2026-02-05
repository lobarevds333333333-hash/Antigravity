from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.main_menu import get_main_menu

router = Router()

from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from keyboards.policy_kb import get_policy_kb

@router.message(CommandStart())
async def process_start_command(message: Message):
    text = (
        "👋 Здравствуйте!\n\n"
        "Я официальный чат-бот частного юриста Лобарева Дмитрия Сергеевича.\n"
        "Для продолжения работы необходимо ознакомиться с Политикой обработки персональных данных."
    )
    
    try:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        photo_path = os.path.join(project_root, "lawyer_avatar.png")
        
        photo = FSInputFile(photo_path)
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=get_policy_kb()
        )
    except Exception as e:
        print(f"Error loading photo: {e}")
        await message.answer(
            text=text,
            reply_markup=get_policy_kb()
        )

@router.callback_query(F.data == "policy_accept")
async def process_policy_accept(callback: CallbackQuery):
    from database import set_user_policy
    await set_user_policy(callback.from_user.id, True)
    
    await callback.message.delete()
    await callback.message.answer(
        text=LEXICON_RU['/start'],
        reply_markup=get_main_menu()
    )

@router.callback_query(F.data == "policy_decline")
async def process_policy_decline(callback: CallbackQuery):
    from database import set_user_policy
    await set_user_policy(callback.from_user.id, False)

    await callback.message.edit_text(
        text="❌ Вы отказались принять Политику. Работа с ботом невозможна.\n\nЕсли передумаете, нажмите кнопку ниже:",
        reply_markup=get_policy_kb()
    )

@router.message(F.text == LEXICON_RU['about_btn'])
async def process_about(message: Message):
    await message.answer(text=LEXICON_RU['about_text'])

@router.message(F.text == LEXICON_RU['services_btn'])
async def process_services(message: Message):
    await message.answer(text=LEXICON_RU['services_text'])

@router.message(F.text == LEXICON_RU['reviews_btn'])
async def process_reviews(message: Message):
    await message.answer(text=LEXICON_RU['reviews_text'], disable_web_page_preview=True)

@router.message(F.text == LEXICON_RU['contacts_btn'])
async def process_contacts(message: Message):
    await message.answer(text=LEXICON_RU['contacts_text'])
