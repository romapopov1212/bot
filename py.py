import telebot
import datetime
import time
import sqlite3
TOKEN = '6553919909:AAHa87zwj1Hl_KHXX2jAh31cGdAHRR_dYeA'
bot = telebot.TeleBot(TOKEN)
updates = bot.get_updates(timeout=60)

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER NOT NULL,
date TEXT NOT NULL
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет Лерочка, введи дату и примерное время когда ты в после раз меняла линзы(желательно в формате 'ГГГГ-ММ-ДД ЧЧ:ММ')")


@bot.message_handler(func=lambda message: True)
def schedule_reminder(message):
    connection = sqlite3.connect('my_database.db')
    cur = connection.cursor()
    try:
        reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M')
        current_time = datetime.datetime.now()
        time_difference = reminder_time + datetime.timedelta(weeks=2) - current_time

        if time_difference.total_seconds() > 0:

            bot.send_message(message.chat.id, f"я запомнил, напомню {reminder_time + datetime.timedelta(weeks=2)})")
            date = reminder_time + datetime.timedelta(weeks=2)
            db_table_val(date)
            cur.execute('SELECT date')
            d = cur.fetchall()
            while(datetime.datetime.now() != d): 
                time.sleep(1)

            bot.send_message(message.chat.id, "ЛЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕРАААААААААААААААААААААААААААААААААААА!!!")
            bot.send_message(message.chat.id, "ЛЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕЕРАААААААААААААААААААААААААААААААААААА!!!!!!!!!!!!!!!!!!!!!!!!")
            bot.send_message(message.chat.id, "передаю от романа, что тебе пора менять линзы, прошло 2 недели🥺")
            bot.send_message(message.chat.id, "если ты только что поменяла линзы, то введи сегодняшнюю дату и время, формат тот же)")
            cur.execute('DELETE FROM Users WHERE id = ?', (1))
            connection.commit()
            cur.close()
            connection.close()
        else:
            bot.send_message(message.chat.id, "Лерочка, 2 недели уже прошли и уже пора менять линзы))")
    except ValueError:
        bot.send_message(message.chat.id, "Ладно Лерочка, не желательно, а обязательно укажи дату в формате 'ГГГГ-ММ-ДД ЧЧ:ММ')")


def db_table_val(user_date: str):
    conn = sqlite3.connect('my_database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO Users (id ,date) VALUES (?, ?)', (1, user_date,))
    conn.commit()
    cur.close()
    conn.close()


bot.infinity_polling(none_stop=True)