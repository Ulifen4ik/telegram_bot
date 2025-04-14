import telebot
import logging
import json
import random
from config import api_token

TOKEN = api_token

bot = telebot.TeleBot(TOKEN)
try:
    with open("user_data.json","r",encoding="utf-8") as file:

        user_data = json.load(file)
except FileNotFoundError:
    user_data = {}


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет!")

@bot.message_handler(commands=["learn"])
def handle_learn(message):
    user_words = user_data.get(str(message.chat.id), {})

    try:
        words_number = int(message.text.split()[1])   
    except IndexError:
        bot.send_message(message.chat.id,"Ведите количество слов")
    try:
        ask_translation(message.chat.id, user_words, words_number)
    except:
        print("Ошибка")
def ask_translation(chat_id, user_words, words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        translation =user_words[word]
        bot.send_message(chat_id, f"Напиши перевод слова {word}.")

        bot.register_next_step_handler_by_chat_id(chat_id, check_translation, translation, words_left)
    else:
        bot.send_message(chat_id, f"Конец урока.")
def check_translation(message, expected_translation, words_left):
    user_translation = message.text.strip().lower()
    if user_translation == expected_translation.lower():
        bot.send_message(message.chat.id, "Правильно! Молодец!")
    else:
        bot .send_message(message.chat.id, f"Неправильно. Верный перевод: {expected_translation}")

    words_left -= 1

    ask_translation(message.chat.id, user_data[str((message.chat.id))], words_left)

    
@bot.message_handler(commands=["addword"])
def handle_addword(message):
    global user_data
    chat_id = message.chat.id
    user_dict = user_data.get(chat_id, {})
    
    words = message.text.split()[1:]
    if len(words) == 2:
        word, translation = words[0].lower(), words[1].lower()
        user_dict[word] = translation

        user_data[chat_id] = user_dict
    
        with open("user_data.json","w",encoding="utf-8") as file:
            json.dump(user_data, file, ensure_ascii=False, indent=4)
        bot.send_message(chat_id, "Слово добавлено в словарь")
    else:
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте еще раз")


@bot.message_handler(func = lambda message: True)
def handle_all(message):
    if message.text.lower() == "как тебя зовут?":
        bot.send_message(message.chat.id, "Y меня пока нет имени")
    if message.text.lower() == "расскажи о себе":
        bot.send_message(message.chat.id, "Я бот для изучения английского языка")
    if message.text.lower() == "расскажи шутку":
        bot.send_message(message.chat.id, "У меня плохое чувство юмора. Советую спросить об этом в интернете")
    if message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, "Хорошо. Я рад, что буду полезным ботом")





def handle_start(message):
    logging.info("Обработчик команды старт")

    bot.send_message(message.chat.id,message.text)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logging.info("Начинаем работу бота")

    bot.polling(non_stop=True)