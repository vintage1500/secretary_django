from warnings import catch_warnings

from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, manager
from keyboards.default import registration_menu
from keyboards.inline import show_static_question_category, start_menu


@bot.message_handler(func=lambda msg: msg.text == "Пройти регистрацию")
def register(message: Message):
    chat_id = message.chat.id
    us_ex = manager.user.user_exists(chat_id)
    if us_ex:
        bot.send_message(chat_id, "Вы уже вошли в систему")
    else:
        bot.send_message(chat_id, f"Введите свои ФИО и номер группы\n"
                                  f"Сообщение должно иметь такой вид:\n"
                                  f"Иванов Иван Иванович\n222-222\n"
                                  f"Все должно быть одним сообщением!", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_new_user)


def get_new_user(message: Message):
    chat_id = message.chat.id
    try:
        student_info = message.text.split()
        last_name = student_info[0]
        first_name = student_info[1]
        patronymic = student_info[2]
        us_group = student_info[3]
        username = message.from_user.username
        manager.user.add_user(last_name, first_name, patronymic, us_group, username, chat_id,)
        bot.send_message(chat_id, f"Регистрация прошла успешно. Здравствуйте, {first_name}", reply_markup=start_menu())
    except Exception as e:
        bot.send_message(chat_id, "Проверьте корректность введенных данных и повторите попытку",
                         reply_markup=registration_menu())


@bot.message_handler(func=lambda msg: msg.text == "Отмена")
def cancel_main_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Без регистрации работа невозможно. Для регистрации введите /start",
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda msg: msg.text == "Часто задаваемые вопросы")
def start_register(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Выберите нужную вам сферу", reply_markup=show_static_question_category())


# @bot.message_handler(func=lambda msg: msg.text == "Задать вопрос")
# def start_ask_question(message: Message):
#     chat_id = message.chat.id
#     bot.send_message(chat_id, f"Введите интересующий вас вопрос\n"
#                               f"В запросе обязательно должны в такой форме:\n"
#                               f"Иванов Иван\n222-222\n*Вопрос*\n"
#                               f"Все должно быть одним сообщением!")
#     bot.register_next_step_handler(message, get_new_question, message.text)


def get_new_question(message: Message):
    chat_id = message.chat.id
    question_text = message.text
    student_info = question_text.split("\n")
    student_name = student_info[0]
    student_group = student_info[1]
    student_question = student_info[2]
    student_username = message.from_user.username
    manager.dynamic_question.add_dynamic_question(student_name, student_group, student_question, student_username,
                                                  chat_id)
    bot.send_message(chat_id, "Вопрос успешно добавлен в базу данных", reply_markup=start_menu())
    # request_new_question(message, message.text)


# @bot.message_handler(func=lambda msg: msg.text == "Принять запрос")
def start_answer_question(message: Message):
    chat_id = message.chat.id
    unanswered_questions = manager.dynamic_question.get_has_dynamic_question()
    number_of_questions = len(unanswered_questions)
    if number_of_questions == 1:
        question_student_name = unanswered_questions[0][0]
        question_student_group = unanswered_questions[0][1]
        question_description = unanswered_questions[0][2]
        question_username = unanswered_questions[0][3]
        text = (f"Был отправлен вопрос от: {question_student_name}\n"
                f"Из группы {question_student_group}\n"
                f"Вопрос: {question_description}\n"
                f"Ссылка на задающего: @{question_username}\n")
        bot.send_message(chat_id, text)

    elif number_of_questions == 0 or number_of_questions is None:
        bot.send_message(chat_id, "Нет сообщений")
    elif number_of_questions > 1:
        pass
    else:
        print("Error in function start_answer_question")
        bot.send_message(chat_id, "Error in function start_answer_question")