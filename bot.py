import telebot
import requests

bot = telebot.TeleBot('7707633432:AAHGmg0YfyD5L_HV5YsQtmn0iVN0rkdpwLs')
API = 'f2372286e88f3ffbb95063b16596bcbf'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет друг! Напиши название города в котором хочешь узнать погоду.')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    try:
        city = message.text.strip().lower()
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
        data = res.json()

        if res.status_code != 200:
            bot.reply_to(message, "Город не найден. Попробуй ещё раз.")
            return

        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]


        bot.reply_to(message, f'Сейчас погода: {temp}°C, {weather_desc}')


        if temp > 20.0:
            image_path = 'солнышко.jpg'
        elif  temp > 10.0:
            image_path = 'тепло.jpg'
        elif temp > 0.0:
            image_path = 'прохладно.jpg'
        elif temp < 0.0:
            image_path: str = 'холод.jpg'
        try:
            with open(image_path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Не удалось загрузить изображение погоды")


        bot.send_message(message.chat.id, 'Если хочешь узнать погоду в другом городе, просто напиши его название)')

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {str(e)}")


bot.polling(none_stop=True)

