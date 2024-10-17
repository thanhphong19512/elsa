import asyncio

from fastapi import FastAPI
from app.controllers.leaderboard_controller import router as leaderboard_router
from fastapi.middleware.cors import CORSMiddleware

from app.kafka_consumer import consume

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def start_kafka_consumer():
    asyncio.create_task(consume())


clients_by_quiz = {}

app.include_router(leaderboard_router)
