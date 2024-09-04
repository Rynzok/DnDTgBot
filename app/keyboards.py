from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Разделить на 2', callback_data='division')],
    [InlineKeyboardButton(text='Умножить на 2', callback_data='multiplication')]
])