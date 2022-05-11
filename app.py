import telebot 
from config import keys, TOKEN
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Бот возвращает курс для выбранной валюной пары.\n\nДля запуска бота, через пробел с большой буквы введите: \n<название валюты, курс которой выхотите узнать> \
<название валюты, по отношению к которой вы хотите узнать курс> \
<количество переводимой валюты>\n\nПример: Доллар Йена 10 \n\nДля вывода списока доступных валют введите: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len (values) != 3:
            raise APIException ('Параметры не соответствуют заданным.')
        
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)   
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена за {amount} {quote} равна {total_base} в {base}'
        bot.send_message(message.chat.id, text)

bot.polling()
