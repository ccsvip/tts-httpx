import os
import mimetypes
import uuid
from datetime import datetime

async def generate_file_name(filename: str) -> str:
    now = datetime.today()
    # 随机的名称 给音频文件使用
    return f"{now.date().year}-{now.date().month}-{now.date().day}-{uuid.uuid4()}-{filename}"

async def check_file_type(content_type:str) -> bool:
    if not content_type.startswith('audio/'):
        return False
    return True

async def get_file_path(file_name: str) -> str:
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    return os.path.join(upload_dir, file_name)

async def get_mime_type(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        raise Exception('无法坚持到文件类型, 请手动指定。')
    
    # MIME 类型标准化映射
    mime_type_mapping = {
        'audio/x-wav': "audio/wav",
        'audio/x-mp3': 'audio/mpeg',
        'audiox-m4a': 'audio/mp4',
    }

    # 如果坚持到的 MIME 类型在映射中， 则使用标准类型
    if mime_type in mime_type_mapping:
        mime_type = mime_type_mapping[mime_type]
    
    return mime_type