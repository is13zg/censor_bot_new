import create_bot
from create_bot import bot
import config
import json

NONE_SET = {"nan", "None", None, "", " ", "NoneType"}
# названия используемых файлов

# здесь хранится список слов которые забанили админы

# база данных
bot_name = "shamil_ahmadullin_helper_bot"

admin_ids = set()


# id админов, далее обновится из бд
async def init_admins():
    global admin_ids
    for chat_id in config.main_chat_ids:
        admins = await bot.get_chat_administrators(chat_id)
        admin_ids.update({admin.user.id for admin in admins})
    admin_ids.add(config.main_chat_anonymous_bot_id)
    admin_ids.add(config.general_chnl_id)
    await create_bot.send_info_message("Current admins:" + str(admin_ids))


#  берем стоп слова из json
def init_bad_words():
    with open(config.BAD_WORDS_FILE, "r") as file:
        tbad_words = json.load(file)
        tbad_words = set(tbad_words["bad_words"])
    return tbad_words


bad_words = init_bad_words()
