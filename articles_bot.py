import telebot
import json
import time
import requests

#необходимо указать токен своего бота, созданного через Botfather
bot = telebot.TeleBot('TOKEN')

def delete_art(art_del, message):
    with open('articles.json', 'r', encoding='utf-8') as file:
        art_list = json.load(file)

    try:
        art_del = int(art_del)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод. Для удаления товара из списка мне нужен только артикул со значком минус. \nПример:\n-18633098")
        return

    if art_del in art_list:
        art_list.remove(art_del)
        bot.send_message(message.chat.id, 'Артикул успешно удален и более не отслеживается')
    else:
        bot.send_message(message.chat.id, 'Данный артикул отсутствует в базе, проверьте ввод')

    with open('articles.json', 'w', encoding='utf-8') as file:
        json.dump(art_list, file, ensure_ascii=False)


def add_art(art, message):
    try:
        art = int(art)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректный ввод. Мне нужен только артикул, ничего больше")
        return

    with open('articles.json', 'r', encoding='utf-8') as file:
        art_list = json.load(file)

    if art in art_list:
        bot.send_message(message.chat.id,'Данный артикул уже добавлен в базу')
    else:
        url = 'https://card.wb.ru/cards/detail?spp=27&nm='
        r = requests.get(f"{url}{art}").content
        text = json.loads(r)

        if text == {"state": 0, "data": {"products": []}}:
            bot.send_message(message.chat.id, 'Был введен некорректный артикул, такого товара не существует (ну или я сломался), проверьте вводимые данные!')
            return

        else:
            title = text.get('data').get('products')[0].get('name')
            price = text.get('data').get('products')[0].get('salePriceU') // 100
            bot.send_message(message.chat.id, f'Товар {title} с текущей ценой {price} рублей добавлен в систему')
            with open('prices.json', 'r', encoding='utf-8') as file:
                dict = json.load(file)

            dict[title] = price

            with open('prices.json', 'w', encoding='utf-8') as file:
                json.dump(dict, file, ensure_ascii=False)

            art_list.append(art)
    with open('articles.json', 'w', encoding='utf-8') as file:
        json.dump(art_list, file, ensure_ascii=False)
        return


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, start_message)


@bot.message_handler(content_types=['text'])
def article(message):
    art = message.text

    if '-' in art:
        art_del = art.replace('-', '')
        delete_art(art_del, message)
    else:
        add_art(art, message)

start_message = 'Добро пожаловать! Я бот, который поможет вам ослеживать самую низкую цену на интересующий вас ' \
                'товар.\nКак я работаю: допустим, вам нужен товар ' \
                'https://www.wildberries.ru/catalog/18633098/detail.aspx пришлите мне отдельным сообщением его ' \
                'артикул \n 18633098\n Для прекращения отслеживания отправьте тот же артикул со знаком ' \
                'минус:\n-18633098 '

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as mes:
        print(mes)
        time.sleep(5)
