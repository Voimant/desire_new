import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from acquaintances_db.db_func import db_bun_users


class AuthoMiddlware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        x = 0
        username = event.from_user.username
        bun = db_bun_users(str(username))
        print(bun)

        if username is None:
            await event.answer(text='Пожалуйста создайте имя пользователя в вашем телеграмм аккаунте,'
                                    ' чтобы пользоваться нашим ботом знакомств\n'
                                    'Как сделайте жмите /start')
        elif bun is True:
            await event.answer(text='Сожалеем, но вы заблокированы админом, для разблокировки обратитесь: @vip_desire_chats\n'
                                    'После повторите команду /start')
        else:
            return await handler(event, data)
