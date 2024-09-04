from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from help import manual
from domain.heros import create_characteristic
from domain.alias import calculation_dice
import app.keyboards as kb
from math import ceil

router = Router()
past_result = 0

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет')


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(manual)


@router.message(F.text)
async def get_cast(message: Message):
    if message.text.lower()[0] == '/':

        msg = message.text.lower()[1::]

        # Создание 6 характеристик персонажа методом броска 4 кубиков
        if msg == 's' or msg == 'scores':
            await message.answer(create_characteristic())

        # Оброботка всех бросков кубика
        elif str(msg).find('d') != -1:
            global past_result
            text, past_result = calculation_dice(msg)

            await message.answer(text, reply_markup=kb.main)

        # # Получение списка всез Алиасов
        # elif msg == 'alias' or msg == 'алиасы' or msg == 'al' or msg == 'ал':
        #     send_some_msg(id, f"{name}, {alias_read_db()}")
        #
        # # Удаление Алиаса
        # elif str(msg).find('del') != -1:
        #     send_some_msg(id, f"{name}, {alis_del_db(msg)}")
        #
        # # Работа с Алиасами
        # elif str(msg).find('al') != -1 or str(msg).find('ал') != -1 and str(msg).find('del') == -1:
        #     try:
        #         # Создание Алиаса
        #         if len(str(msg).split()) > 2:
        #             send_some_msg(id, f"{name}, {create_alias(msg)}")
        #         # Активация Алиаса
        #         else:
        #             send_some_msg(id, f"{name}, {alias_release(msg)}")
        #     except:
        #         send_some_msg(id, f"{name}, Где-то есть ошибка")
        #
        # else:
        #     send_some_msg(id, f"{name}, Не попало в ifы")

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
