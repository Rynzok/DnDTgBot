from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, PollAnswer
from aiogram.fsm.context import FSMContext

from help import manual
from domain.heros import create_characteristic
from domain.alias import calculation_dice, alias_release, create_alias, alias_read_db
import app.keyboards as kb
from math import ceil
from infrastructure.work_with_db import alis_del_db
from app.states import CreateHero

router = Router()
past_result = 0

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет \n id чата: {message.chat.id}\n Название группы: {message.chat.full_name}')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(manual)

@router.message(Command('create'))
async def create_hero_one(message: Message, state: FSMContext):
    await state.set_state(CreateHero.main)
    await message.answer("Введите: Имя Песрнонажа, Класс, Расу, Уровень, Название предыстории, Мировозрение \n"
                         "Пример: Лирой, Варвар, Полуорк, 4, Отшельник, Хаотично-злой")

@router.message(CreateHero.main)
async def create_hero_second(message: Message, state: FSMContext):
    await state.update_data(main = message.text)
    await state.set_state(CreateHero.characteristic)
    await message.answer("Введите 6 значений характеристик персонажа в порядке: Сила, Ловкость, Толосложение, "
                         "Интеллект, Мурдость, Харизма \n"
                         "Пример: 16, 14, 15, 12, 10, 11")

@router.message(CreateHero.characteristic)
async def create_hero_second(message: Message, state: FSMContext):
    await state.update_data(characteristic = message.text)
    await state.set_state(CreateHero.skill)
    data = await state.get_data()
    await message.answer(f"Установите галочки в прокаченных навыках, а пока вы ввели: {data}")
    await message.answer_poll(question='Спасброски?',
                              options=['Сила', 'Ловкость', 'Телосложение', 'Интеллект', 'Мудрость', 'Харизма'],
                              is_anonymous=False,
                              allows_multiple_answers=True)

@router.poll_answer()
async def poll_res(pa: PollAnswer):
    chat_id = pa.user.id
    await pa.bot.send_message(chat_id=chat_id, text=f"{pa.option_ids}, {pa.user.id}")


@router.message(F.text)
async def get_cast(message: Message):
    if message.text.lower()[0] == '/':
        global past_result
        msg = message.text.lower()[1::]

        # Создание 6 характеристик персонажа методом броска 4 кубиков
        if msg == 's' or msg == 'scores':
            await message.answer(create_characteristic())

        # Оброботка всех бросков кубика
        elif msg.find('d') != -1 and msg.find('al') == -1:

            text, past_result = calculation_dice(msg)
            await message.answer(text, reply_markup=kb.main)

        # Получение списка всез Алиасов
        elif msg == 'alias' or msg == 'алиасы' or msg == 'al' or msg == 'ал':
            await message.answer(f"{alias_read_db(message.chat.id)}")

        # Удаление Алиаса
        elif str(msg).find('del') != -1:
            try:
                text = alis_del_db(msg, message.chat.id)
            except Exception:
                text = "Неверное имя Алиаса либо ещё что-то пошло не так"
            await message.answer(f"{text}")

        # Работа с Алиасами
        elif msg.find('al') != -1 and msg.find('del') == -1:
            # Создание Алиаса
                if len(msg.split()) > 2:
                    text, past_result = create_alias(msg, message.chat.id)
                    await message.answer(f"{text}", reply_markup=kb.main)
                # Активация Алиаса
                else:
                    try:
                        text, past_result = alias_release(msg, message.chat.id)
                    except Exception:
                        text = "Неверное имя Алиаса либо другая ошибка"
                        past_result = 0
                    await message.answer(f"{text}", reply_markup=kb.main)
        else:
            await message.answer('Что-то пошло не так')

    # await message.answer(f'У меня всё хорошо')


@router.callback_query(F.data == 'division')
async def division(callback: CallbackQuery):
    await callback.answer('')
    global past_result
    past_result = ceil(past_result / 2)
    await callback.message.edit_text(f'Новый резльтат: {past_result}', reply_markup=kb.main)


@router.callback_query(F.data == 'multiplication')
async def division(callback: CallbackQuery):
    await callback.answer('')
    global past_result
    past_result = past_result * 2
    await callback.message.edit_text(f'Новый резльтат: {past_result}', reply_markup=kb.main)
