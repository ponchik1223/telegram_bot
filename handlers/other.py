from aiogram import types, Dispatcher
from create_bot import dp

help_message = """
    <b>список команд поддерживаемых ботом:</b>
/weather - <em>узнать погоду в городе</em>
/currency - <em>конвертировать сумму в валюту</em>
/animal_day - <em>картинка с лисой</em>
/survey - <em>создать опрос</em>
/help - <em>помощь</em>

(Напишите <b>"выход/exit"</b>, чтобы покинуть опцию)
"""
# обработчик сообщения /help
async def help_send(message: types.Message):
    if message.chat.type == "private":
        await message.answer(text=help_message)
    else:
        await message.reply(text=help_message)

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(help_send, commands=["help"])