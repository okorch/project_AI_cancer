from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

import  time, logging


TOKEN = '6066040431:AAH1dQUsLwu5icMLloR-46VHNwfbeRuB_S8'

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name

    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    chat_id = message.chat.id
    text = f"Hi dear, {user_full_name}!\n Upload a picture."

    await bot.send_message(chat_id=chat_id, text=text)



if __name__ == '__main__':
    executor.start_polling(dp)