import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from redis import asyncio as aioredis
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


logger = logging.getLogger(__name__)


# redis地址
redis_url = "redis://localhost"
# 数据队列
queue_key = "autoText"
pool = aioredis.ConnectionPool.from_url(redis_url)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动前的操作
    redis = aioredis.Redis.from_pool(pool)
    await redis.delete(queue_key)
    await redis.aclose()
    
    yield
    
    # 关闭时的操作
    await pool.aclose()


app = FastAPI(lifespan=lifespan)


# 自定义全局错误信息
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=200, content={"code": 0, "msg": "请求失败"})


# 自定义全局错误信息
@app.exception_handler(RequestValidationError)
async def request_validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=200, content={"code": 0, "msg": "请求失败"})


# 收到任务提交
@app.post("/api/sendMsg")
async def post(data: dict):
    # 获取消息内容
    msg = data.get('msg')
    receiver = data.get('receiver')

    if msg and receiver:
        try:
            # 从应用状态获取连接池
            redis = aioredis.Redis.from_pool(pool)
            # 推入到队列
            await redis.lpush(queue_key, json.dumps({"receiver": receiver, "msg": msg}))
            queue_size = await redis.llen(queue_key)
            await redis.aclose()
            return {"code": 1, 'taskId': queue_size, 'msg': '任务提交成功'}
        except Exception as e:
            logger.error(f"添加消息到队列失败: {str(e)}")
            return {"code": 0, 'msg': '系统繁忙，请稍后重试'}
    else:
        return {"code": 0, 'msg': '参数异常'}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
