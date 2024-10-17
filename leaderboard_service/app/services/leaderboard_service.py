import redis
from app.dtos.leaderboard_dto import LeaderboardDTO


class LeaderboardService:
    def __init__(self):
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=True)

    async def get_leaderboard(self, quiz_id: str):
        # Fetch top 10 from Redis sorted set using the quiz_id
        leaderboard_key = f"leaderboard:{quiz_id}"
        leaderboard = self.redis.zrevrange(leaderboard_key, 0, 9, withscores=True)
        leaderboard_dto = LeaderboardDTO.from_redis(quiz_id, leaderboard)

        return leaderboard_dto.to_dict()
