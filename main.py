import logging
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from config import API_TOKEN
from database import Database
from buttons import *

# for state
from aiogram.dispatcher import FSMContext
from state import UserData
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
db = Database()
admin = 5222507821

# create baza
db.create_table_users()

# Define a command handler
@dp.message_handler(commands=['start'], state='*')
async def echo(message: types.Message, state: FSMContext):    
    telegram_id = message.from_user.id
    data = db.select_users(telegram_id)
    if data is None:
        username = message.from_user.username
        await state.update_data(telegram_id=telegram_id)
        await state.update_data(username=username)
        await message.reply("Assalomu alekum! Ismingizni yozing....")
        await UserData.name.set()
    else:
        await message.reply("Siz ro'yxatdan o'tgansiz!")

@dp.message_handler(state=UserData.name)
async def echo(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer("Telefon raqamingizni yuboring...", reply_markup=phone_number)
    await UserData.phone.set()

@dp.message_handler(content_types='contact', state=UserData.phone)
async def echo(message: types.Message, state: FSMContext):
    phone_number = message.contact['phone_number']
    await state.update_data(phone=phone_number)
    await message.answer("Joylashuvingizni yuboring...", reply_markup=location)
    await UserData.next()    

@dp.message_handler(content_types='location', state=UserData.location)
async def echo(message: types.Message, state: FSMContext):
    print(message.location)
    location = f"{message.location['latitude']} {message.location['longitude']}"
    await state.update_data(location=location)

    data = await state.get_data()
    # print(data)
    telegram_id_ = data['telegram_id']
    username_ = data['username']
    name_ = data['name']
    phone_ = data['phone']
    location_ = data['location']

    db.insert_users(telegram_id_, username_, name_, phone_, location_)
    await message.answer("Siz ro'yxatdan muvaffaqiyatli o'tdingiz!")
    await bot.send_message(admin, f"New user from @testuseer_bot\n\nName: {name_}\nUsername: @{username_}\nID: {telegram_id_}\nPhone number: +{phone_}")
    await state.finish()
    await state.reset_state()

# Run the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)