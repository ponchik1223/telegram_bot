from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import requests
from random import randint
import os
from create_bot import dp, bot

#класс всех состояний бота
class ProfileStateGroup(StatesGroup):
    name_city = State()
    currency = State()
    
class RootProfileStateGroup(StatesGroup):
    query = State()
    answer = State()

# Обработчик команды /start  
async def start_cmd_handler(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['/weather', '/currency', '/animal_day', '/survey']
    keyboard_markup.add(*buttons)
    await message.answer("Привет! Что вам нужно?", reply_markup=keyboard_markup)

#/////////////////////////////////////////////////////////////////////
# Обработчик команды /погода
async def weather_cmd_handler(message: types.Message):
    await message.answer("В каком городе вы бы хотели узнать погоду?")
    await ProfileStateGroup.name_city.set()
    

# Обработчик сообщения с названием города
@dp.message_handler(state=ProfileStateGroup.name_city)
async def weather_handler(message: types.Message, state: FSMContext):

    if message.text.lower() in ['выход','exit']:
            await message.answer("Рад был помочь!")
            await state.finish()
    else:  
        
        try:
            # создаем словарь для записи необходимых параметров
            answer_dict = dict()
            # получаем название города и переводим его в нижний регистр
            city_name = message.text.lower()
            # редактируем название
            for item in ["-", " "]:
                city_name = city_name.replace(item,"+")
            
            # получаем свой ключ, делаем запрос, формируем json
            api_key = os.getenv('OpenWeatherMap_Key')
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ru'
            response = requests.get(url).json()
            
            # вытаскиваем необходимые нам данный 
            feels_like = round(response["main"]["feels_like"])
            temp = round(response['main']['temp'])
            wind = round(response["wind"]["speed"])
            desc = response['weather'][0]['description'] 

            #записываем данные в наш словарь
            answer_dict["Текущаяя температура: "] = str(temp) + "°С"
            answer_dict["Ощущается как "] = str(feels_like) + "°С"
            answer_dict["Скорость ветра: "] = str(wind) + "м/с"
            answer_dict["Тип погоды: "] = desc
            
            # формирум строку ответа
            answer = "" 
            for item in answer_dict:
                answer += f"{item} {answer_dict[item]}\n"       
            
            await message.answer(answer)
        except:
            await message.answer("Произошла ошибка. Проверьте название города.")
        
#/////////////////////////////////////////////////////////////////////
# Обработчик команды /currency
async def currency_cmd_handler(message: types.Message):
    await message.answer("Какую валюту ты хочешь конвертировать? (Формат запроса: 50 USD EUR)")
    await ProfileStateGroup.currency.set()
    

# Обработчик сообщения с валютами
@dp.message_handler(state=ProfileStateGroup.currency)
async def currency_handler(message: types.Message, state: FSMContext):
    if message.text.lower() in ['выход','exit']:
            await message.answer("Рад был помочь!")
            await state.finish()
    else:  
        try:
            num, from_currency, to_currency = message.text.upper().split()
            api_key = os.environ.get('CURRENCY_API_KEY')
            url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}'
            response = requests.get(url).json()
            rate = float(response['conversion_rate'])
            await message.answer(f"{num} {from_currency} = {round(rate * float(num), 2)} {to_currency}")
        except:
            await message.answer("Произошла ошибка. Некорректный ввод!")

#/////////////////////////////////////////////////////////////////////
# Обработчик команды /animals
async def animals_cmd_handler(message: types.Message):
    id_photo = randint(1,121)
    await bot.send_photo(chat_id=message.chat.id, photo=f"https://randomfox.ca/images/{id_photo}.jpg")
#/////////////////////////////////////////////////////////////////////


# Обработчик команды /survey
async def poll_cmd_handler(message: types.Message):
    await message.answer(text="<b>Какой вопрос выносим на обсуждение?</b>")
    await RootProfileStateGroup.query.set() 

@dp.message_handler(state=RootProfileStateGroup.query)
async def query_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["query"] = message.text
    await message.answer("перечислите варианты ответов через запятую")
    await RootProfileStateGroup.next()

@dp.message_handler(state=RootProfileStateGroup.answer)
async def poll_handler(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['answer'] = message.text.split(",")
        await bot.send_poll(chat_id=message.chat.id, question=data["query"], options=data["answer"])
        await state.finish()
    except:
        wrong_text = f"""
{message.text} - некорректный ввод!
Перечислите варианты ответов через <b>запятую!</b>
        """
        await message.answer(text=wrong_text)

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(start_cmd_handler, commands=["start", "restart"])
    dp.register_message_handler(weather_cmd_handler, commands=['weather'])
    dp.register_message_handler(currency_cmd_handler, commands=['currency'])
    dp.register_message_handler(animals_cmd_handler, commands=['animal_day'])
    dp.register_message_handler(poll_cmd_handler, commands=['survey'])
