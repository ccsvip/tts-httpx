import os
import time
import httpx
from typing import Optional
from fastapi import HTTPException

from core.tts import TTS
from core.chat import Chat
from config import BASE_URL, API_KEY
from api.dependencies import get_mime_type

async def audio_to_text(file_path: str) -> str:
    url = f'{BASE_URL}/audio-to-text'
    headers = {
        'Authorization': f"Bearer {API_KEY}"
    }

    try:
        mime_type = await get_mime_type(file_path)
        async with httpx.AsyncClient() as client:
            with open(file_path, 'rb') as f:
                files = {
                    'file': (os.path.basename(file_path), f, mime_type),
                }
                response = await client.post(url, headers=headers, files=files)
                # response.raise_for_status()
                return response.json().get('text')
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f'错误: 找不到文件 {file_path}')
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f'请求出错: {e}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"其他错误: {e}")

async def send_requests(text:str) -> str:
    try:
        chat = Chat()
        text_content = await chat.send_request(text)
        print(f'文本内容: \n{text_content}')
        return text_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型请求失败: {str(e)}")

async def tts_request(text:str, file_path: Optional[str]=None) -> None:
    try:
        tts = TTS()
        await tts.tts_request(text, file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'TTS 请求失败: {str(e)}')
    