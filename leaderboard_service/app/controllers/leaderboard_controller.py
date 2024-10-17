from fastapi import APIRouter, Query
from app.services.leaderboard_service import LeaderboardService

router = APIRouter()
leaderboard_service = LeaderboardService()


@router.get("/leaderboard")
async def get_leaderboard(quiz_id: str = Query(...)):
    return await leaderboard_service.get_leaderboard(quiz_id)
