from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from data.loader import manager, bot


def registration_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(
        KeyboardButton(text="Пройти регистрацию"),
        KeyboardButton(text="Отмена")
    )
    return markup
