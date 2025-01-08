import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints import router as api_router
from config import PORT

app = FastAPI(
    title='Hander Audio API',
    description='处理音频相关的接口, 使用的是dify提供的api key.',
    version='1.0.0',
    docs_url='/',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE'], # 明确指定允许的HTTP方法
    allow_headers=['*'],
)

app.include_router(api_router, prefix='/v1')

if __name__ == "__main__":
    # 忽略特定的链接错误
    logging.getLogger('uvicorn.error').handlers.clear()

    # 配置日志级别
    uvicorn_logger = logging.getLogger('uvicorn')
    uvicorn_logger.setLevel(logging.WARNING)
    uvicorn.run('main:app', host='0.0.0.0', port=PORT, reload=True)