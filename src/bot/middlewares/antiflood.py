from typing import Any, Callable, Awaitable
import time

from aiogram import BaseMiddleware
from aiogram.types import Message


def rate_limit(limit: int, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator


class Throttled(Exception):
    def __init__(self, **kwargs):
        self.key = kwargs.pop('key', '<None>')
        self.called_at = kwargs.pop('LAST_CALL', time.time())
        self.rate = kwargs.pop('RATE_LIMIT', None)
        self.exceeded_count = kwargs.pop('EXCEEDED_COUNT', 0)
        self.delta = kwargs.pop('DELTA', 0)
        self.user = kwargs.pop('user', None)
        self.chat = kwargs.pop('chat', None)

    def __str__(self):
        return f'Rate limit exceeded! (Limit: {self.rate} s, ' \
                f'exceeded: {self.exceeded_count}, ' \
                f'time delta: {round(self.delta, 3)} s)'


class CancelHandler(Exception):
    pass


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=0.5, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        self.throttle_manager = ThrottleManager()
        super(ThrottlingMiddleware, self).__init__()

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        try:
            await self.on_process_event(event, data)
        except CancelHandler:
            return
        result = await handler(event, data)
        return result

    async def on_process_event(
        self,
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        limit = getattr(data['handler'].callback, 'throttling_rate_limit', self.rate_limit)
        key = getattr(data['handler'].callback, 'throttling_key', f'{self.prefix}_message')
        try:
            await self.throttle_manager.throttle(key, rate=limit, user_id=event.from_user.id, chat_id=event.chat.id)
        except Throttled as t:
            await self.event_throttled(event, t)
            await event.delete()
            raise CancelHandler()

    async def event_throttled(self, event: Message, throttled: Throttled):
        if throttled.exceeded_count <= 2:
            return


class ThrottleManager:
    bucket_keys = [
        'RATE_LIMIT', 'DELTA',
        'LAST_CALL', 'EXCEEDED_COUNT'
    ]

    def __init__(self):
        self.data_store = {}

    async def throttle(self, key: str, rate: float, user_id: int, chat_id: int):
        now = time.time()
        bucket_name = f'throttle_{key}_{user_id}_{chat_id}'
        data = self.data_store.get(bucket_name, {
            'RATE_LIMIT': rate,
            'LAST_CALL': now,
            'DELTA': 0,
            'EXCEEDED_COUNT': 0
        })
        called = data.get('LAST_CALL', now)
        delta = now - called
        result = delta >= rate or delta <= 0
        data['RATE_LIMIT'] = rate
        data['LAST_CALL'] = now
        data['DELTA'] = delta
        if not result:
            data['EXCEEDED_COUNT'] = data.get('EXCEEDED_COUNT', 0) + 1
        else:
            data['EXCEEDED_COUNT'] = 1
        self.data_store[bucket_name] = data
        if not result:
            raise Throttled(key=key, chat=chat_id, user=user_id, **data)
        return result
