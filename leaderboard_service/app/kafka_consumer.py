import asyncio
import requests
from aiokafka import AIOKafkaConsumer
import redis
from app.config import KAFKA_TOPIC, KAFKA_BOOTSTRAP_SERVERS, KAFKA_GROUP_ID, REDIS_HOST, REDIS_PORT, REDIS_DECODE_RESPONSES

from app.dtos.leaderboard_dto import LeaderboardDTO


async def consume():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID
    )

    max_retries = 5
    retry_count = 0
    retry_delay = 5

    while retry_count < max_retries:
        try:
            print("Trying to connect...")
            await consumer.start()
            print("Kafka consumer connected.")
            break
        except Exception as e:
            retry_count += 1
            print(
                f"Failed to connect, retrying...")
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, 60)

    if retry_count == max_retries:
        print("Max retries reached. Failed to connect to Kafka.")
        return

    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=REDIS_DECODE_RESPONSES)

        async for msg in consumer:
            quiz_id = msg.value.decode()

            # Get top 10 users
            leaderboard_key = f"leaderboard:{quiz_id}"
            top_10 = redis_client.zrevrange(leaderboard_key, 0, 9, withscores=True)

            leaderboard_dto = LeaderboardDTO.from_redis(quiz_id, top_10)
            try:
                response = requests.post(
                    f"http://host.docker.internal:8002/update_leaderboard",
                    json=leaderboard_dto.to_dict()
                )
                response.raise_for_status()
                print(f"Leaderboard data sent for {quiz_id}")
            except Exception as e:
                print(f"Failed to send leaderboard data to WebSocket service: {e}")

    finally:
        await consumer.stop()
        print("Kafka consumer stopped.")
