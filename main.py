from create_bot import bot, dp
import asyncio
import init_data
from handlers import admin, censor_handler, admin_changes_in_group


async def main() -> None:


    dp.include_router(admin.router)
    dp.include_router(censor_handler.router)
    dp.include_router   (admin_changes_in_group.router)

    await init_data.init_admins()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
