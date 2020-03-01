from HozRequest import db_functions as dbf
import telebot


bot = telebot.TeleBot('1122591052:AAFIYn2JtecLqHhgVB8p1XPw9hnh8P1mu4A')


initial_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
initial_keyboard.row('Войти', 'Регистрация')

waiting_for_login = dict()
waiting_for_password = dict()
logged = dict()
users = dict()


@bot.message_handler(commands=['start'])
def start_message(message):
    print("Got /start")
    bot.send_message(message.chat.id, 'Начало работы с ботом', reply_markup=initial_keyboard)


@bot.message_handler(func=lambda message: waiting_for_login.get(message.from_user.id, False) == True, content_types=['text'])
def get_login(message):
    print("GET LOGIN")
    users[message.from_user.id] = dict()
    users[message.from_user.id]["login"] = message.text
    waiting_for_login[message.from_user.id] = False
    waiting_for_password[message.from_user.id] = True
    bot.send_message(message.chat.id, 'Введите пароль')


@bot.message_handler(func=lambda message: waiting_for_password.get(message.from_user.id, False) == True, content_types=['text'])
def get_password(message):
    print("GET PASSWORD")
    users[message.from_user.id]["password"] = message.text
    waiting_for_password[message.from_user.id] = False
    login = users[message.from_user.id]["login"]
    password = users[message.from_user.id]["password"]
    login_message = dbf.login(login, password)
    if login_message != 'Successful log in':
        bot.send_message(message.chat.id, login_message + " Try to log in again or register.")
    else:
        bot.send_message(message.chat.id, login_message)
        logged[message.from_user.id] = True


@bot.message_handler(func=lambda message: logged.get(message.from_user.id, False) == False, content_types=['text'])
def handle_conversation(message):
    print("Got message")
    if message.text == 'Войти':
        bot.send_message(message.chat.id, 'Введите email')
        waiting_for_login[message.from_user.id] = True
        print("Login request")
    if message.text == 'Регистрация':
        print("1300 bucks")
        bot.send_message(message.chat.id, 'http://127.0.0.1:8000/signup')


@bot.message_handler(func=lambda message: logged.get(message.from_user.id, False), content_types=['text'])
def conversation(message):
    print(message.text.split())
    if message.text.lower() == 'публичные проблемы':
        for problem in dbf.get_public_problems():
            print(problem)
            bot.send_message(message.chat.id, f'id -- {problem["id"]}, theme -- {problem["theme"]}')
        print('public problems requested')
    elif message.text.lower() == 'мои проблемы':
        for problem in dbf.get_problems_by_user(users[message.from_user.id]['login']):
            print(problem)
            bot.send_message(message.chat.id, f'id -- {problem["id"]}, theme -- {problem["theme"]}')
        print('user problems requested')
    elif message.text.lower().startswith('текст проблемы') and len(message.text.split()) == 3:
        try:
            print(dbf.get_problems_by_id(int(message.text.split()[-1]))[0]['problem_text'])
            print('problem requested')
            bot.send_message(message.chat.id, dbf.get_problems_by_id(int(message.text.split()[-1]))[0]['problem_text'])
        except ValueError:
            pass
    elif message.text.lower().startswith('получить сообщения') and len(message.text.split()) == 3:
        try:
            print('comments requested')
            print(dbf.get_comments(int(message.text.split()[-1])))
            for i, comment in enumerate(dbf.get_comments(int(message.text.split()[-1]))):
                if i % 2:
                    bot.send_message(message.chat.id, f'{users[message.from_user.id]["login"]}:\n--{comment["message_text"]}')
                else:
                    bot.send_message(message.chat.id, f'--{comment["message_text"]}')
        except ValueError:
            pass


# @bot.message_handler(commands=['start'])
# def start_message(message):
#     print("Got /start")
#     bot.send_message(message.chat.id, 'Начало работы с ботом', reply_markup=initial_keyboard)


def run_bot():
    bot.polling()
