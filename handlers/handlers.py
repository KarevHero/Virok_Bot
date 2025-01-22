from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from parser import parser
from keyboard import cell_promotion


router = Router()

@router.message(F.text == 'Новинки 🔥 от 9 Грудня')
async def sell(message: Message):
    await message.answer(text='Выбирите из списка', reply_markup=cell_promotion.new_keyboard.as_markup(resize_keyboard=True))

@router.message(F.text.startswith('🔥'))
async def sell_part(message: Message):
    await message.answer(text='Формирую запрос...')
    await parser.new_part_parser(message)

# @router.message(F.text.startswith('💰'))
# async def sell_part(message: Message):
#     await message.answer(text='Формирую запрос...')
#     await parser.sell_part_parser(message)
#
#
# @router.message(F.text == 'Распродажа 💰')
# async def sell(message: Message):
#     await message.answer(text='Выбирите из списка', reply_markup=cell_promotion.sale_keyboard.as_markup(resize_keyboard=True))

@router.message(F.text == 'Акции от 28 фев')
async def sell(message: Message):
    photo1 = FSInputFile('sale_and_new/Cell.jpg')
    photo2 = FSInputFile('sale_and_new/Hat.jpg')
    await message.answer_photo(photo=photo1, caption='Шланги')
    await message.answer_photo(photo=photo2, caption='Шапки зимние')

@router.message()
async def mess(message: Message):
    await parser.get_info(message)




