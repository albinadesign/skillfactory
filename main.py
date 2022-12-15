# telegram bot "currency rates"

import telebot
from config import keys, TOKEN
from extensions import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)
        if len(values) != 3:
            raise APIException('Введите три параметра:\n<имя валюты> \
                <в какую валюту перевести> \
                <количество переводимой валюты> ')
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду. Попробуйте еще раз\n{e}')
    else:

        text = f'{quote} в количестве {amount} равен  {total_base * float(amount)} в валюте {base}'
        bot.send_message(message.chat.id, text)


bot.polling()