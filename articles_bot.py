import telebot
import json
import time
import requests

#необходимо указать токен своего бота, созданного через Botfather
bot = telebot.TeleBot('TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать! Пришлите мне артикул товара, который вы хотите отслеживать')

@bot.message_handler(content_types=['text'])
def article(message):
    art = message.text
    try:
        art = int(art)
    except Exception as mes:
        print('Ошибка при вводе', mes)
        bot.send_message(message.chat.id, "Некорректный ввод. Мне нужен только артикул, ничего больше")
        return

    with open('articles.json', 'r', encoding='utf-8') as read_test:
        art_list = json.load(read_test)

    if art in art_list:
        bot.send_message(message.chat.id,'Данный артикул уже добавлен в базу')
        
    else:
        url = 'https://card.wb.ru/cards/detail?spp=27&nm='
        r = requests.get(f"{url}{art}").content
        
        text = json.loads(r)
        
        if text == {"state": 0, "data": {"products": []}}:
            bot.send_message(message.chat.id, 'Был введен некорректный артикул, такого товара не существует (ну или я сломался), проверьте вводимые данные')
            return
            
        else:
            title = text.get('data').get('products')[0].get('name')
            price = text.get('data').get('products')[0].get('salePriceU') // 100
            
            bot.send_message(message.chat.id, f'Товар {title} с текущей ценой {price} рублей добавлен в систему')
            
            with open('prices.json', 'r', encoding='utf-8') as read_test:
                dict = json.load(read_test)
                
            dict[title] = price
            
            with open('prices.json', 'w', encoding='utf-8') as write_test:
                json.dump(dict, write_test, ensure_ascii=False)
                
        art_list.append(art)
        
    with open('articles.json', 'w', encoding='utf-8') as write_test:
        json.dump(art_list, write_test, ensure_ascii=False)
        return


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as mes2:
        print('Общая ошибка бота при пуллинге:', mes2)
        time.sleep(5)