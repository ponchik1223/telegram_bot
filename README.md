# Проект чат-бота в Telegram

Данный бот позволяет использовать следующие функции:

## Выдача случайной картинки лисы

Чтобы получить случайную картинку лисы, отправьте команду `/animal_day`. Для реализации этой функции в проекте используется API сайта https://randomfox.ca/.

## Конвертирование валюты

Чтобы конвертировать валюту, отправьте команду `/currency`. Далее отправьте боту "число валюта валюта" и он ответит конвертированым числом. Для реализации этой функции в проекте изпользуется сайт https://www.exchangerate-api.com/

## Выдача прогноза погоды

Чтобы получить прогноз погоды, отправьте команду `/weather`. Далее бот запросит уточнение по городу. Для реализации этой функции в проекте используется API сайта https://openweathermap.org/.

## Создание опросов

Чтобы создать опрос в чате, отправьте команду `/survey`. Далее бот запросит вопрос и список вариантов ответов. Для реализации этой функции в проекте используется библиотека `aiogram`.

## Функция помощи

Чтобы получить список доступных команд, отправьте команду `/help`.

## Установка и запуск

Для запуска бота необходимо установить окружение, описанное в `requirements.txt`. 
Для этого выполните команду `pip install -r requirements.txt`. 

Далее создайте bash скрипт для запуска бота

```
source /venv/bin/activate # активируйте окружение среды
cd pwd/bot # зайдите в папку с ботом
export TOKEN=YOUR_TOKEN_TELEGRAM # создайте перменные с вашими ключами
export OpenWeatherMap_Key=YOUR_TOKEN_API
export CURRENCY_API_KEY=YOUR_TOKEN_API
python3 bot.py  # запустите бота
```

