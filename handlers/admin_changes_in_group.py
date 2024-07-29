from aiogram import F, Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, KICKED, LEFT, \
    RESTRICTED, MEMBER, ADMINISTRATOR, CREATOR
from aiogram.types import ChatMemberUpdated
import init_data

import config
import create_bot

router = Router()
router.chat_member.filter(F.chat.id == config.main_chat_id)


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=
        (KICKED | LEFT | RESTRICTED | MEMBER)
        >>
        (ADMINISTRATOR | CREATOR)
    )
)
async def admin_promoted(event: ChatMemberUpdated):
    init_data.admin_ids.add(event.new_chat_member.user.id)
    await create_bot.send_info_message(f"{event.new_chat_member.user.first_name} "
                                       f"был(а) повышен(а) до Администратора!")


@router.chat_member(
    ChatMemberUpdatedFilter(
        # Обратите внимание на направление стрелок
        # Или можно было поменять местами объекты в скобках
        member_status_changed=
        (KICKED | LEFT | RESTRICTED | MEMBER)
        <<
        (ADMINISTRATOR | CREATOR)
    )
)
async def admin_demoted(event: ChatMemberUpdated):
    init_data.admin_ids.discard(event.new_chat_member.user.id)
    await create_bot.send_info_message(
        f"{event.new_chat_member.user.first_name} "
        f"был(а) понижен(а) до обычного юзера!"
    )
