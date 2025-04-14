import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import django
from django.core.wsgi import get_wsgi_application
import environ

# Инициализация Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secretary_faculty.settings')
django.setup()
application = get_wsgi_application()

from questions.models import Question

# Загрузка переменных окружения
env = environ.Env()
environ.Env.read_env()

# Инициализация бота
bot = telebot.TeleBot(env('TELEGRAM_BOT_TOKEN'))

# Состояния пользователей
user_states = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("Абитуриент", callback_data='applicant'),
        InlineKeyboardButton("Студент", callback_data='student')
    )
    bot.send_message(
        message.chat.id,
        "Добро пожаловать! Пожалуйста, выберите ваш статус:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data in ['applicant', 'student']:
        user_states[call.from_user.id] = {'user_type': call.data}
        bot.send_message(
            call.from_user.id,
            "Спасибо! Теперь напишите ваш вопрос:"
        )
        bot.register_next_step_handler(call.message, save_question)

def save_question(message):
    try:
        chat_id = message.chat.id
        if chat_id in user_states:
            user_type = user_states[chat_id]['user_type']
            question_text = message.text
            
            if not question_text.strip():
                bot.send_message(chat_id, "Вопрос не может быть пустым. Пожалуйста, напишите ваш вопрос:")
                bot.register_next_step_handler(message, save_question)
                return
            
            Question.objects.create(
                user_type=user_type,
                question_text=question_text
            )
            
            bot.send_message(
                chat_id,
                "Спасибо за ваш вопрос! Мы рассмотрим его в ближайшее время."
            )
            del user_states[chat_id]
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(
            chat_id,
            "Произошла ошибка при обработке вашего вопроса. Пожалуйста, попробуйте позже."
        )

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()