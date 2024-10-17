from typing import List, Dict


class LeaderboardDTO:
    def __init__(self, quiz_id: str, leaderboard: List[Dict[str, float]]):
        self.quiz_id = quiz_id
        self.leaderboard = leaderboard

    def to_dict(self):
        return {
            "quiz_id": self.quiz_id,
            "leaderboard": self.leaderboard
        }

    @classmethod
    def from_redis(cls, quiz_id: str, redis_data: List[tuple]):
        leaderboard = [{"username": user, "score": score} for user, score in redis_data]
        return cls(quiz_id, leaderboard)
