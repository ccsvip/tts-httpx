FROM python:3.11

WORKDIR /app

# 首先只复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple

# 然后再复制其他文件
COPY . .

# 加载 .env 文件中的环境变量
ARG PORT
ENV PORT=${PORT}

CMD uvicorn run:app --host 0.0.0.0 --port ${PORT} --reload