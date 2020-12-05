import get_hw
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '1432648425:AAECn_Bt89nHzS_XFN2PFRGNYtHKGUQaL4g'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
lentayevo_id = '-1001486134019'

btn_what_day_tomorrow = InlineKeyboardButton(text='На завтра?', callback_data='Tom')
btn_what_day_not_tomorrow = InlineKeyboardButton(text='Другой день', callback_data='NotTom')
markup = InlineKeyboardMarkup(row_width=2).row(btn_what_day_tomorrow, btn_what_day_not_tomorrow)

ids = ''
@dp.message_handler(commands=['hw'])
async def hw(message: types.Message):
    global ids
    ids = message.chat.id
    await bot.send_message(message.chat.id, 'Выберете дату', reply_markup=markup)
    ids = message.chat.id

@dp.message_handler(commands=['helps'])
async def helps(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите команду "/hw" или дату в формате dd.mm.yyyy')

@dp.callback_query_handler(text='NotTom')
@dp.callback_query_handler(text='Tom')
async def tom_date(query: types.callback_query):
    text='s'
    answer_data = query.data
    if answer_data == 'Tom':
        text = get_hw.get_hw(get_hw.check_day())
    elif answer_data == 'NotTom':
        text = 'Введите дату в формате dd.mm.yyyy'
    if query.from_user.id == lentayevo_id:
        await bot.send_message(lentayevo_id, text)
    else:
        await bot.send_message(query.from_user.id, text)
@dp.message_handler()
async def check_message(message: types.Message):
    try:
        await bot.send_message(message.chat.id, get_hw.get_hw(message.text))
    except:
        pass
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
