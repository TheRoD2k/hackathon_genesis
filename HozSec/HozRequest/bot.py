import db_functions as dbf
import telebot


bot = telebot.TeleBot('1122591052:AAFIYn2JtecLqHhgVB8p1XPw9hnh8P1mu4A')


initial_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
initial_keyboard.row('Войти', 'Регистрация')

waiting_for_login = {}
waiting_for_password = {}
logged = {}

users = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    print("Got /start")
    bot.send_message(message.chat.id, 'Начало работы с ботом', reply_markup=initial_keyboard)



@bot.message_handler(lambda message: waiting_for_login[message.from_user.id] == True)
def get_login(message):
    users[message.from_user.id]["login"] = message.text
    waiting_for_login[message.from_user.id] = False
    waiting_for_password[message.from_user.id] = True


@bot.message_handler(lambda message: waiting_for_password[message.from_user.id] == True)
def get_password(message):
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


@bot.message_handler(lambda message : login[message.from_user.id] == False, content_types=['text'])
def handle_conversation(message):
    print("Got message")
    if message.text == 'Войти':
        waiting_for_login[message.from_user.id] = True
        print("Login request")
    if message.text == 'Регистрация':
        print("300 bucks")
        bot.send_message(message.chat.id, 'http://127.0.0.1:8000/signup')


bot.polling()
