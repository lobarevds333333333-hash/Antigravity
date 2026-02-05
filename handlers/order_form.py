from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from config import config
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.contact_kb import request_contact_kb
from keyboards.main_menu import get_main_menu

router = Router()

class FSMConsultation(StatesGroup):
    fill_name = State()
    fill_phone = State()
    fill_time = State()
    fill_desc = State()

@router.message(F.text == LEXICON_RU['consultation_btn'])
async def start_consultation(message: Message, state: FSMContext):
    from database import get_user_policy
    from keyboards.policy_kb import get_policy_kb
    
    is_accepted = await get_user_policy(message.from_user.id)
    
    if not is_accepted:
        await message.answer(
            text="⚠️ Для записи на консультацию необходимо принять Политику обработки данных.",
            reply_markup=get_policy_kb()
        )
        return

    await message.answer(text='Как к вам обращаться?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(FSMConsultation.fill_name)

@router.message(StateFilter(FSMConsultation), F.text.casefold().in_({'отмена', 'cancel'}))
async def cancel_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('❌ Заявка отменена', reply_markup=get_main_menu())

@router.message(StateFilter(FSMConsultation.fill_name))
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text='Пожалуйста, укажите ваш номер телефона.\n(Можно нажать кнопку ниже)',
        reply_markup=request_contact_kb()
    )
    await state.set_state(FSMConsultation.fill_phone)

@router.message(StateFilter(FSMConsultation.fill_phone))
async def process_phone(message: Message, state: FSMContext):
    contact = message.contact
    if contact:
        phone = contact.phone_number
    else:
        phone = message.text
    
    await state.update_data(phone=phone)
    await message.answer(
        text='В какое время вам удобно принять звонок?\n(Например: "Завтра после 14:00")',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(FSMConsultation.fill_time)

@router.message(StateFilter(FSMConsultation.fill_time))
async def process_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer(text='Кратко опишите, что случилось?')
    await state.set_state(FSMConsultation.fill_desc)

@router.message(StateFilter(FSMConsultation.fill_desc))
async def process_desc(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(desc=message.text)
    data = await state.get_data()
    
    from database import add_lead
    await add_lead(
        telegram_id=message.from_user.id,
        name=data.get('name'),
        phone=data.get('phone'),
        time=data.get('time'),
        description=data.get('desc')
    )

    user_alias = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
    admin_text = (
        f"🔔 Новая заявка на консультацию!\n\n"
        f"👤 Имя: {data.get('name')}\n"
        f"📞 Телефон: {data.get('phone')}\n"
        f"⏰ Удобное время: {data.get('time')}\n\n"
        f"❓ Суть вопроса:\n{data.get('desc')}\n\n"
        f"🔗 Профиль: {user_alias}"
    )

    for admin_id in config.ADMIN_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=admin_text)
        except Exception:
            pass

    await message.answer(
        text='Спасибо! Ваша заявка на консультацию передана в работу.',
        reply_markup=get_main_menu()
    )
    await state.clear()
