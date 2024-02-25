from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
            self,
            handler,
            event,
            data
    ) -> Any:
        self.counter += 1
        print(self.counter)
        data['counter'] = self.counter
        return await handler(event, data)
