from aiogram.types import   KeyboardButton, ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📝 Регистрация'),
         KeyboardButton(text='👤 Мои данные')],
        [KeyboardButton(text='✏️ Изменить данные'), KeyboardButton(text='🗑 Удалить данные')],
        [KeyboardButton(text='👥 Все студенты')]
    ],
    resize_keyboard=True
)
