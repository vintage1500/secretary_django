from telebot.types import Message
from data.loader import bot, manager
from keyboards.default import registration_menu
from keyboards.inline import start_menu, start_administrator_menu


@bot.message_handler(commands=['start'], chat_types='private')
def start(message: Message):
    chat_id = message.chat.id
    first_name = manager.user.get_first_name(chat_id)
    text = f"Здравствуйте"
    user_administrator = manager.user.get_is_user_administrator(chat_id)
    if user_administrator is None or not user_administrator[0]:
        if first_name:
            text += f", {first_name[0]}, я чат-бот, созданный в рамках учебного проекта «Чат-боты для Московского " \
                    f"Политеха». Моя задача — помочь вам быстро получать нужную информацию и решать вопросы" \
                    f" в удобном формате."
            bot.send_message(chat_id, text, reply_markup=start_menu())
        else:
            text += ". Перед использованием необходимо пройти регистрацию.\n"
            bot.send_message(chat_id, text, reply_markup=registration_menu())
    else:
        text += f", {first_name[0]}. У вас роль администратора!"
        bot.send_message(chat_id, text, reply_markup=start_administrator_menu())
