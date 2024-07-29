from aiogram import Bot, Dispatcher, Router
import config
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

TOKEN = config.BotToken
dp = Dispatcher()
router = Router()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def send_debug_message(name, func, exc):
    await bot.send_message(config.Support_chat_id, f"Module: {name}\n"
                                                   f"Func: {func}\n"
                                                   f"Excep: {exc}\n")



async def send_info_message(info):
    await bot.send_message(config.Support_chat_id, info)


def print_error_message(name, func, exc):
    print(f"Module: {name}\n"
          f"Func: {func}\n"
          f"Excep: {exc}\n")
