import os
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, Request, Path
from fastapi.responses import FileResponse

from api.utils import audio_to_text, send_requests, tts_request
from api.dependencies import generate_file_name, check_file_type, get_file_path, get_mime_type

router = APIRouter()

@router.get('/tts/{file_name}', summary='获取音频', description='获取音频文件名称', tags=['TTS相关接口'])
async def get_audio(file_name: str):
    file_path = await get_file_path(file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="文件不存在")
    mime_type = await get_mime_type(file_path)
    # return file_path
    return FileResponse(file_path, media_type=mime_type) 

@router.get('/tts', summary='获取所有音频', description='获取所有音频文件', tags=['TTS相关接口'])
async def get_all_files() -> List[str]:
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    if not os.path.exists(upload_dir):
        raise []
    return os.listdir(upload_dir)

@router.post('/tts', summary='上传音频', description='上传音频并返回访问URL', tags=['TTS相关接口'])
async def upload_audio(audio_file: UploadFile=File(...), request:Request=None):
    try:
        if not await check_file_type(audio_file.content_type):
            raise HTTPException(status_code=400, detail='只能上传音频文件')
        
        file_name = await generate_file_name(audio_file.filename)
        file_path = await get_file_path(file_name)
        
        with open(file_path, 'wb') as buffer:
            buffer.write(await audio_file.read())

        text = await audio_to_text(file_path)
        text = await send_requests(text)
        await tts_request(text, file_path)

        base_url = str(request.base_url).rstrip('/')
        return {'url': f'{base_url}/v1/tts/{file_name}'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'处理音频失败: {str(e)}')


@router.delete('/tts/{file_name}', summary='删除音频', description='删除音频文件', tags=['TTS相关接口'])
async def remove_file(file_name: str=Path(..., description="要删除的音频文件的名称，例如 'abc.mp3'")):
    try:
        file_path = await get_file_path(file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return {'message': f'文件【{file_name}】删除成功'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'删除文件失败: {str(e)}')

@router.delete('/tts', summary='删除所有音频', description='删除所有音频文件', tags=['TTS相关接口'])    
async def remove_all_files():
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    print(upload_dir)
    try:
        if os.path.exists(upload_dir):
            for file in os.listdir(upload_dir):
                print(f'file: {file}')
                os.remove(os.path.join(upload_dir, file))
            return {'message': "所有文件删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'删除文件失败: {str(e)}')


@router.post("/v1/chat", summary="通过模型获取文本回答", description="通过模型获取文本回答", tags=["文本接口"])
async def chat_with_model(text: str):
    try:
        response_text = await send_requests(text)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"请求失败: {str(e)}")
