from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from sale_and_new import sale

# cell_button = KeyboardButton(text='Распродажа 💰')
promotion = KeyboardButton(text='Акции от 28 фев')
new_art = KeyboardButton(text='Новинки 🔥 от 9 Грудня')
main_keyboard = ReplyKeyboardMarkup(keyboard=[[promotion, new_art]], resize_keyboard=True)

# sale_keyboard = ReplyKeyboardBuilder()
# sale_buttons = [KeyboardButton(text=f'💰c {i} до {i+9}') for i in range(1, len(sale.sale), 10)]
# sale_keyboard.row(*sale_buttons, width=3)

new_keyboard = ReplyKeyboardBuilder()
new_buttons = [KeyboardButton(text=f'🔥c {i} от {sale.new_art_list[i][-1]}') for i in range(1, len(sale.new_art), 10)]
new_keyboard.row(*new_buttons, width=3)