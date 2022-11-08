import telebot
import json
import time
import requests

#необходимо указать токен своего бота, созданного через Botfather
bot = telebot.TeleBot('TOKEN')


while True:
    
    with open('articles.json', 'r', encoding='utf-8') as read_art:
        articles = json.load(read_art)

    for elem in articles:
        url = 'https://card.wb.ru/cards/detail?spp=27&nm='
        r = requests.get(f"{url}{elem}").content
        
        text = json.loads(r)
        
        title = text.get('data').get('products')[0].get('name')
        price = text.get('data').get('products')[0].get('salePriceU')//100
        average_price = text.get('data').get('products')[0].get('averagePrice')//100
        benefit = text.get('data').get('products')[0].get('benefit')
        
        with open ('prices.json', 'r', encoding='utf-8') as read_test:
            dict = json.load(read_test)
            if dict.get(title):
                if dict[title] > price:
                    # на данный момент информация о снижении цены публикуется в канале с id -1001881473314 ( https://t.me/pupperprices ), 
                    # можно заменить на любой другой, в том числе и просто себе в личку 
                    bot.send_message('-1001881473314', f'Товар {title} подешевел на {dict[title] - price} рублей. \n'
                                                       f'Актуальная цена: {price}.\n'
                                                       f'Средняя цена на данный товар на ВБ: {average_price}\n'
                                                       f'Выгода: {benefit}%\n'
                                                       f'Ссылка на товар: https://www.wildberries.ru/catalog/{elem}/detail.aspx')
                    dict[title] = price
                    
            else:
                dict[title] = price
                
        with open('prices.json', 'w', encoding='utf-8') as write_test:
            json.dump(dict, write_test, ensure_ascii=False)
        
        time.sleep(420)
