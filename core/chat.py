import httpx
import json
from config import API_KEY, BASE_URL

class Chat:
    __slots__ = ['api_key', 'base_url']

    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL
    
    async def send_request(self, text:str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "inputs": [],
            "query": text,
            "response_mode": "streaming",
            "conversation_id": "",
            "user": 1
        }

        chat_message_url = f"{self.base_url}/chat-messages"
        text_content = ""
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    'POST',
                    url=chat_message_url,
                    headers=headers,
                    json=data,
                    timeout=30
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                json_data = json.loads(line.replace('data:', '').strip())
                                if answer := json_data.get('answer'):
                                    text_content += answer
                            except json.JSONDecodeError as e:
                                raise Exception(f'JSON解析错误: {e}')

        except httpx.RequestError as e:
            raise Exception(f'请求失败: {str(e)}')
        except Exception as e:
            raise Exception(f'处理失败: {str(e)}')
        
        text_content = text_content.replace('Final Answer:', '') # 模型默认会回复前缀
        return text_content
