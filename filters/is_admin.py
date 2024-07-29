from aiogram.filters import BaseFilter
from aiogram.types import Message
import init_data


class IsAdmin(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in init_data.admin_ids
