import asyncio
from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery


class AuthoMiddlware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        x = 0
        username = event.from_user.username
        if username is None:
            await event.answer(text='Пожалуйста создайте имя пользователя в вашем телеграмм аккаунте,'
                                    ' чтобы пользоваться нашим ботом знакомств\n'
                                    'Как сделайте жмите /start')
        else:
            return await handler(event, data)
