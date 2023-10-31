from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

phone_number = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton("📞 Telefon raqamni yuborish!", request_contact=True)  
        ]
    ],
    resize_keyboard=True
)

location = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton("📍 Joylashuvni yuborish", request_location=True)
        ]
    ],
    resize_keyboard=True
)

