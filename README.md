Сервис представлен двумя ботами для телеграма, общее назначение которых в отслеживании изменений цены заданных товаров в сторону уменьшения.
Первый бот ( articles_bot.py ) собирает артикулы от пользователя и добавляет их в json файл, из которого второй бот ( price_wb.py ) берет артикул и
последовательно в бесконечном цикле проходит по каждому из них, проверяя цену. При уменьшении цены - приходит оповещение в заданный канал/личное 
сообщение пользователю. 

Также в репозитории содержатся файлы для systemd для ubuntu серверов (на каждый из ботов), при помощи которых создаются демоны, контроллирующие 
непрерывную работу скрипта. 

To do list:
-Изучить асинхронное программирование на Python, чтобы можно было безболезненно объединить два сервиса в один
-Продумать рандомизацию заголовков запросов цены. На данный момент ВБ позволяет с одного айпи и одного и того же user-агента запрашивать цену, но так не будет всегда
-Хранить данные не в Json файлах, а использовать БД.