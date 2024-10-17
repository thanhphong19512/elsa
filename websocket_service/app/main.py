from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients_by_quiz = {}


@app.get("/health")
async def health_check():
    return {"status": "Service is healthy"}


@app.websocket("/ws/{quiz_id}")
async def websocket_endpoint(websocket: WebSocket, quiz_id: str):
    await websocket.accept()

    if quiz_id not in clients_by_quiz:
        clients_by_quiz[quiz_id] = []

    clients_by_quiz[quiz_id].append(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        clients_by_quiz[quiz_id].remove(websocket)
        if not clients_by_quiz[quiz_id]:
            del clients_by_quiz[quiz_id]


@app.post("/update_leaderboard")
async def update_leaderboard(request: Request):
    data = await request.json()
    quiz_id = data.get("quiz_id")
    leaderboard_data = data.get("leaderboard")
    if quiz_id in clients_by_quiz:
        for websocket in clients_by_quiz[quiz_id]:
            try:
                await websocket.send_json(leaderboard_data)
            except Exception as e:
                print(f"Failed to send data to WebSocket: {e}")

    return {"status": "success"}
