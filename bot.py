from aiogram.utils import executor
from create_bot import dp
from handlers import client, other

# отправляем в командную строку сообщение о запуске
async def on_start(_):
    print("Автобот в интернете!")

client.register_handlers_client(dp)
other.register_handlers_other(dp)

# создаем точку входа
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
