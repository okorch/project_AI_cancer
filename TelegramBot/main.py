from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor, markdown
from aiogram.types import ParseMode
import time, logging
import config
from TelegramBot import secret_key

TOKEN = secret_key.TOKEN

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    '''
    This function handles the '/help' command and sends a list of avaliable commands.
    Args:
        message (types.Message): User's message object.
    Returns:
        None
    '''
    commands = [
        markdown.text(markdown.bold('/start'), ' - start the bot'),
        markdown.text(markdown.bold('/help'), ' - show help'),
        markdown.text(markdown.bold('/info'), ' - show information about the bot')
    ]
    commands_text = markdown.text('Available commands:\n', '\n'.join(commands))
    await message.reply(commands_text, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    '''
    This function handles the '/start' command and sends a welcome message to the user.
    Args:
        message (types.Message): User's message object.
    Returns:
        None
    '''
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    chat_id = message.chat.id

    text = f"Hi dear, {user_full_name}!\n\n"\
    'This bot was made to analyze photos of histological preparations for the presence of cancer cells.\n\n ' \
    'To analyze a photo, send it in a message. If you need to check several photos, send them one photo at ' \
    'a time. To find out what else this bot can do, call the command /help'

    await bot.send_message(chat_id=chat_id, text=text)

@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    '''
    This function handles the '/info' command and sends an information about bot.
    Args:
        message (types.Message): User's message object.
    Returns:
        None
    '''
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    chat_id = message.chat.id
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    with open('info', 'r') as file:
        text = file.read()

    await bot.send_message(chat_id, text= text, parse_mode='Markdown')

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def photo(message: types.Message):
    '''
    This function handles photo messages from the user and sends a response message based on the photo.
    Args:
        message (types.Message): User's message object containing a photo.
    Returns:
        None
    '''
    chat_id = message.chat.id
    photos = message.photo[-1]
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    file = await photos.get_file()
    stream = await bot.download_file(file.file_path)
    image = await config.process_photo(stream)
    text = 'Photo successfully downloaded!'
    await bot.send_message(chat_id=chat_id, text=text)

    result = await config.predict(image)
    if result == 1:
        text = 'Cancer'
        await bot.send_message(chat_id=chat_id, text=text)
    else:
        text = 'No cancer'
        await bot.send_message(chat_id=chat_id, text=text)

if __name__ == '__main__':
    executor.start_polling(dp)