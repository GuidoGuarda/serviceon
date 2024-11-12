# video_service.py

def create_video_room(room_name):
    # Lógica para criar uma sala de vídeo
    print(f"Room '{room_name}' created.")
    return {"room_name": room_name, "status": "created"}

def generate_access_token(user_id, room_name):
    # Lógica para gerar um token de acesso
    print(f"Access token for user {user_id} in room {room_name} generated.")
    return {"user_id": user_id, "room_name": room_name, "access_token": "some_token_value"}
