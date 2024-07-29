from create_bot import bot
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
import config
import create_bot
import inspect
from filters.is_admin import IsAdmin
import init_data
import datetime
import json
from aiogram.types import FSInputFile


router = Router()


@router.message(Command(commands=["ban"]), IsAdmin())
async def cmd_ban(msg: Message):
    try:
        if not msg.reply_to_message:
            await msg.reply("Эта команда должна быть ответом на сообщение!")
            return
        await msg.delete()
        # print(msg.reply_to_message.from_user)
        await bot.send_message(msg.chat.id, f" @{msg.reply_to_message.from_user.first_name} banned.")
        await msg.bot.ban_chat_member(chat_id=msg.chat.id, user_id=msg.reply_to_message.from_user.id,
                                      until_date=datetime.timedelta(days=10))
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


@router.message(Command(commands=["add_bad"]))
async def new_bad_words(msg: Message):
    try:
        new_bad_words = set(map(str.lower, msg.text.split()[1:]))
        bad_words2 = init_data.bad_words.union(new_bad_words)
        if init_data.bad_words == bad_words2:
            await bot.send_message(msg.chat.id,
                                   "Слова НЕ добавлены. Текущий список:\n" + (" ").join(init_data.bad_words))
        else:
            init_data.bad_words = bad_words2
            new_dict = dict()
            new_dict["bad_words"] = list(init_data.bad_words)
            with open(config.BAD_WORDS_FILE, "w") as file:
                json.dump(new_dict, file)
            await bot.send_message(msg.chat.id, "Слова добавлены. Текущий список:\n" + (" ").join(init_data.bad_words))
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


@router.message(Command(commands=["del_bad"]), IsAdmin())
async def del_bad_words(msg: Message):
    try:
        new_bad_words = set(map(str.lower, msg.text.split()[1:]))
        new_bad_words = init_data.bad_words.difference(new_bad_words)

        if (new_bad_words == init_data.bad_words):
            await bot.send_message(msg.chat.id,
                                   "Ничего не удалено, в списке не было тех слов что вы написали. Текущий список:\n" + (
                                       " ").join(init_data.bad_words))
            return
        else:
            init_data.bad_words = new_bad_words
            new_dict = dict()
            new_dict["bad_words"] = list(init_data.bad_words)
            with open(config.BAD_WORDS_FILE, "w") as file:
                json.dump(new_dict, file)

            await bot.send_message(msg.chat.id, "Слова удалены.Текущий список:\n" + (" ").join(init_data.bad_words))
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


@router.message(Command(commands=["helppp"]), IsAdmin())
async def helppp(msg: Message):
    try:
        await msg.reply(
            """
    По команде /new_bad можно добавить одно или несколько стоп-слов через пробел, данные слова нельзя будет использовать обычным пользователям в чате
    По команде /del_bad можно удалить одно или несколько стоп-слов через пробел
    По команде /ban можно забанить пользователя на 10 дней.Нужно ответить на его сообщение
    По команде /reserv можно получить файл ограничений
            """
        )
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


@router.message(Command(commands=["reserv"]), IsAdmin())
async def make_reserv_data(msg: Message):
    try:
        await bot.send_document(msg.chat.id, FSInputFile(config.BAD_WORDS_FILE))

    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)
