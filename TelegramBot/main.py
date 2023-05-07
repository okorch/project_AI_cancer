from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import torch.nn as nn
import torch.nn.functional as F  # Functional
from PIL import Image

import torchvision.transforms as transforms

import time, logging


TOKEN = '6066040431:AAH1dQUsLwu5icMLloR-46VHNwfbeRuB_S8'

bot = Bot(token = TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name

    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    chat_id = message.chat.id
    text = f"Hi dear, {user_full_name}!\n Upload one picture."

    await bot.send_message(chat_id=chat_id, text=text)



@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def photo(message: types.Message):
    chat_id = message.chat.id
    photos = message.photo[-1]
    file = await photos.get_file()
    stream = await bot.download_file(file.file_path)
    image = await process_photo(stream)
    text = 'Photo successfully downloaded!'
    await bot.send_message(chat_id=chat_id, text=text)

async def process_photo(stream):
    image = Image.open(stream)
    image = transforms.ToTensor()(image)
    image = transforms.Resize((64, 64))(image)
    return image
async def analysis_photo(image, weight_matrix):

def predict(model, data, target):
    model.eval()
    data, target = data.cuda(), target.cuda()
    output = model(data)
    pr = output.detach().cpu().numpy()
    return pr

if __name__ == '__main__':
    executor.start_polling(dp)