import base64
import json
import os
import uuid

from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, status
from sqlalchemy.exc import SQLAlchemyError
from mysite.database.db import SessionLocal
from mysite.clients.auth import verify_access_token
from mysite.database.models import Group, GroupMessage, GroupPeople


websocket_router = APIRouter(prefix='/ws', tags=['Websocket'])

# Папка для загруженных файлов (создаётся автоматически при старте)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Максимальный размер файла — 10 МБ (можно поменять под себя)
MAX_FILE_SIZE = 10 * 1024 * 1024


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, group_id: int, websocket: WebSocket):
        await websocket.accept()
        if group_id not in self.active_connections:
            self.active_connections[group_id] = []
        self.active_connections[group_id].append(websocket)

    async def disconnect(self, group_id: int, websocket: WebSocket):
        connections = self.active_connections.get(group_id)
        if not connections:
            return
        if websocket in connections:
            connections.remove(websocket)
        if not connections:
            self.active_connections.pop(group_id, None)

    async def broadcast(self, group_id: int, data: dict):
        connections = self.active_connections.get(group_id, [])
        disconnect_connections = []

        for i in connections.copy():
            try:
                await i.send_json(data)
            except RuntimeError:
                disconnect_connections.append(i)

        for i in disconnect_connections:
            await self.disconnect(group_id, i)


manager = ConnectionManager()


@websocket_router.websocket("/group/{group_id}")
async def group_chat_websocket(websocket: WebSocket, group_id: int, access_token: str):
    try:
        current_user = await verify_access_token(access_token)
    except HTTPException as error:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason=str(error.detail))
        return

    db = SessionLocal()
    try:
        group_db = db.query(Group).filter(Group.id == group_id).first()
        if not group_db:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Мындай группа жок")
            return

        member_db = (
            db.query(GroupPeople)
            .filter(GroupPeople.group_id == group_id, GroupPeople.user_id == current_user['id'])
            .first()
        )
        if not member_db:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason='Сиз бул группада жоксуз')
            return
    finally:
        db.close()

    await manager.connect(group_id, websocket)

    await websocket.send_json(
        {
            "type": "connection.established",
            "data": {
                "group_id": group_id,
                "user": current_user['id'],
                "username": current_user['username'],
            },
        }
    )

    try:
        while True:
            raw = await websocket.receive_text()

            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({
                    'type': 'error',
                    "detail": "Туура эмес формат. JSON күтүлгөн.",
                })
                continue

            msg_type = payload.get("type", "text")

            db = SessionLocal()
            message_data = None
            try:
                if msg_type == "text":
                    text = (payload.get("message") or "").strip()

                    if not text:
                        await websocket.send_json({
                            'type': 'error',
                            "detail": "Билдируу бош болбошу керек",
                        })
                        continue

                    if len(text) > 5000:
                        await websocket.send_json({
                            'type': 'error',
                            "detail": "Билдируу 5000 белгиден ашпашы керек",
                        })
                        continue

                    message_db = GroupMessage(
                        group_id=group_id,
                        user_id=current_user['id'],
                        message=text,
                    )

                elif msg_type == "file":
                    file_name = payload.get("file_name")
                    file_type = payload.get("file_type", "application/octet-stream")
                    file_data_b64 = payload.get("file_data")

                    if not file_name or not file_data_b64:
                        await websocket.send_json({
                            'type': 'error',
                            "detail": "Файл маалыматтары толук эмес (file_name же file_data жок)",
                        })
                        continue

                    try:
                        file_bytes = base64.b64decode(file_data_b64)
                    except Exception:
                        await websocket.send_json({
                            'type': 'error',
                            "detail": "Файл base64 форматында эмес",
                        })
                        continue

                    if len(file_bytes) > MAX_FILE_SIZE:
                        await websocket.send_json({
                            'type': 'error',
                            "detail": f"Файл өтө чоң (максимум {MAX_FILE_SIZE // (1024 * 1024)}MB)",
                        })
                        continue

                    ext = os.path.splitext(file_name)[1]
                    stored_name = f"{uuid.uuid4().hex}{ext}"
                    stored_path = os.path.join(UPLOAD_DIR, stored_name)

                    with open(stored_path, "wb") as f:
                        f.write(file_bytes)

                    file_url = f"/uploads/{stored_name}"

                    message_db = GroupMessage(
                        group_id=group_id,
                        user_id=current_user['id'],
                        file_url=file_url,
                        file_name=file_name,
                        file_type=file_type,
                        file_size=len(file_bytes),
                    )

                else:
                    await websocket.send_json({
                        'type': 'error',
                        "detail": "Белгисиз билдируу түрү (type: 'text' же 'file' болушу керек)",
                    })
                    continue

                db.add(message_db)
                db.commit()
                db.refresh(message_db)

                message_data = {
                    "type": "message.created",
                    "data": {
                        "id": message_db.id,
                        "group_id": message_db.group_id,
                        "user": message_db.user_id,
                        "username": current_user['username'],
                        "message": message_db.message,
                        "file_url": message_db.file_url,
                        "file_name": message_db.file_name,
                        "file_type": message_db.file_type,
                        "file_size": message_db.file_size,
                        "created_date": str(message_db.created_date),
                    },
                }

            except SQLAlchemyError:
                db.rollback()
                await websocket.send_json({
                    'type': 'error',
                    "detail": "Билдируу сакталган жок",
                })
                continue
            finally:
                db.close()

            if message_data:
                await manager.broadcast(group_id, message_data)

    except WebSocketDisconnect:
        await manager.disconnect(group_id, websocket)