from aiogram.dispatcher.filters.state import State, StatesGroup

class UserData(StatesGroup):
    telegram_id = State()  
    username = State()  
    name = State()  
    phone = State()  
    location = State()  