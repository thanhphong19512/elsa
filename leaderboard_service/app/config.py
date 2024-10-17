# Kafka settings
KAFKA_TOPIC = 'score_change'
KAFKA_BOOTSTRAP_SERVERS = 'host.docker.internal:9092'
KAFKA_GROUP_ID = 'leaderboard-consumer'

# Redis settings
REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DECODE_RESPONSES = True
