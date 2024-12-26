import asyncio
import json
from profile.app import db, settings
from profile.core.amqp.tester import AsyncAMQPConnectionTester
from profile.logger import get_logger
from profile.user_profile.models import UserProfile

import aio_pika
from aio_pika.exchange import ExchangeType

logger = get_logger(__name__)


async def handler(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        body = json.loads(message.body)
        if body["type"] == "SEND_VERIFY_EMAIL":
            user_id = body["userId"]
            new_user = UserProfile(user_id=user_id)
            async with db.begin() as session:
                session.add(new_user)
            logger.info(f"New user created: ID={user_id}...")


async def main():
    connection = await aio_pika.connect_robust(settings.user_events.url())
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            name=settings.user_events.exchange,
            type=ExchangeType.TOPIC,
            passive=False,
            durable=True,
            auto_delete=False,
        )
        queue = await channel.declare_queue("client_user_events")
        await queue.bind(exchange, routing_key=settings.user_events_routing_key)
        await queue.consume(handler)

        logger.info("[*] Waiting for logs. To exit press CTRL+C")
        try:
            await asyncio.Future()
        finally:
            await connection.close()


if __name__ == "__main__":
    tester = AsyncAMQPConnectionTester(settings.user_events)
    loop = asyncio.new_event_loop()
    is_connected = loop.run_until_complete(tester.wait())
    if not is_connected:
        raise ConnectionError("Not Connected")
    logger.info("Starting main...")
    asyncio.run(main())
