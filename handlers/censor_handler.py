from aiogram import types
import create_bot
import init_data
from censure import Censor
from create_bot import bot
import time
import string
import inspect
from aiogram.enums.content_type import ContentType
from aiogram.types import ChatPermissions
from mat import mat_list
from aiogram import Router
from filters.is_admin import IsAdmin
import config

router = Router()


def get_message_link(tlg_msg: types.Message) -> str:
    # Преобразование chat_id из формата -100xxxxxxxxxx в формат, используемый в ссылках
    chat_id = tlg_msg.chat.id
    if str(chat_id).startswith("-100"):
        chat_id = str(chat_id)[4:]
    return f"https://t.me/c/{chat_id}/{tlg_msg.message_id}"


# отправка сообщение и ограничение по времени
async def ban_action_and_msg(tlg_msg, text, ban_msg, ban_time=5):
    try:
        await bot.send_message(config.Support_chat_id,
                               text=f" @{tlg_msg.from_user.username} написал:{text}\n его забанили")
        await bot.send_message(tlg_msg.chat.id,
                               ban_msg + f"Вы не сможете отправлять собщения в чат {str(ban_time)} минут")
        await bot.restrict_chat_member(tlg_msg.chat.id, tlg_msg.from_user.id,
                                       permissions=ChatPermissions(can_send_messages=False),
                                       until_date=time.time() + ban_time * 60)
        await tlg_msg.delete()
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


#  предупреждение насчет матов
async def warning_msg(tlg_msg, text, to_attention):
    try:
        await bot.send_message(config.Support_chat_id,
                               text=f"@{tlg_msg.from_user.username} написал:\n{text}\n{get_message_link(tlg_msg)}\nПод подозрением:\n{to_attention}")

    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)


# обработчик фильтр сылок, матов ,персылок
# @dp.message_handler(IsNotAdmin(), content_types=types.ContentTypes.ANY)
@router.message(~IsAdmin())
async def moderate_message(msg: types.Message):
    try:
        # check forwarding
        if msg.forward_from:
            await ban_action_and_msg(msg, str(msg), f" @{msg.from_user.username} Пересылка сообщений запрещена.", 5)
            return

        if msg.content_type == ContentType.NEW_CHAT_MEMBERS:
            await msg.delete()

        text = ""
        if msg.caption != None:
            text += msg.caption + " "
        if msg.text != None:
            text += msg.text

        if text == "":
            return

        if len(text) < 3:
            await warning_msg(msg, text, 'too_short')

        # check urls

        entities_types = set()
        if msg.entities != None:
            for entity in msg.entities:
                entities_types.add(entity.type)

            if len(entities_types.intersection(
                    {"mention", "url", "text_link", "phone_number", "email", "text_mention"})) > 0:
                await ban_action_and_msg(msg, text,
                                         f" @{msg.from_user.username} Отправка ссылок, номеров, email в чат запрещена.",
                                         10)
                return

            # check censor
        censor_ru = Censor.get(lang='ru')
        censor_ls = censor_ru.clean_line(text)
        # мат нашелся
        if censor_ls[1] != 0:
            if len(set(map(lambda x: str(x).lower(), censor_ls[3])).intersection(mat_list)) != 0:
                old_ls_text = text.split()
                censor_ls_text = censor_ls[0].split()
                new_msg = list()

                for x in range(len(old_ls_text)):
                    if censor_ls_text[x] == "[beep]":
                        new_msg.append("*" * len(old_ls_text[x]))
                    else:
                        new_msg.append(old_ls_text[x])
                new_str = " ".join(new_msg)
                await ban_action_and_msg(msg, text,
                                         f" @{msg.from_user.username} написал:\n" + new_str + "\nРугательства запрещены.",
                                         10)
                return
            else:
                await warning_msg(msg, text, ' '.join(censor_ls[3]))

        if (len({word.lower().translate(str.maketrans('', "", string.punctuation)) for word in
                 text.split(" ")}.intersection(init_data.bad_words)) != 0):
            await ban_action_and_msg(msg, text, f" @{msg.from_user.username} ваше сообщение запрещено.", 10)
            return
    except Exception as e:
        await create_bot.send_debug_message(__name__, inspect.currentframe().f_code.co_name, e)
