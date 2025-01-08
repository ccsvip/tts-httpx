import httpx
from typing import Optional
from config import API_URL, REFERENCE_ID

class TTS:

    __slots__ = ['api_url', 'reference_id']

    def __init__(self):
        self.api_url = API_URL
        self.reference_id = REFERENCE_ID

    async def tts_request(self, content_text: str, file_path: Optional[str]=None):
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    'POST',
                    self.api_url + '/v1/tts',
                    json={'text': content_text, "reference_id": self.reference_id},
                    timeout=None
                ) as response:
                    if response.status_code != 200:
                        error_content = (await response.aread().decode())
                        raise Exception(f'Error: {response.status_code} - {error_content}')
                    with open(file_path, 'wb') as file:
                        async for chunk in response.aiter_bytes():
                            file.write(chunk)
        except Exception as e:
            raise Exception(f'TTS 请求失败 {str(e)}')