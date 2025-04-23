import asyncio
import json
import logging
from redis import asyncio as aioredis
from wxauto import WeChat

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

# redis连接池
pool = aioredis.ConnectionPool.from_url(redis_url)

# 微信实例
wx = WeChat()


async def process_task(task_data: str):
    try:
        logger.info("开始处理任务：" + task_data)
        task = json.loads(task_data)
        receiver = task.get('receiver')
        msg = task.get('msg')

        if not receiver or not msg:
            logger.error(f"无效的任务数据: {task_data}")
            return

        wx.SendMsg(msg, receiver)
        logger.info("处理成功！")

    except json.JSONDecodeError:
        logger.error(f"解析任务数据失败: {task_data}")
    except Exception as e:
        logger.error(f"处理任务时发生错误: {str(e)}")


async def main():
    """主函数：监听消息队列并处理消息"""
    redis = None
    try:
        # 创建Redis连接
        redis = aioredis.Redis.from_pool(pool)
        logger.info("消息队列服务启动成功")

        while True:
            try:
                # 从队列获取消息，设置5秒超时
                task = await redis.brpop([queue_key], timeout=5)
                if task:
                    await process_task(task[1].decode('utf-8'))
            except asyncio.CancelledError:
                logger.info("收到停止信号，正在关闭服务...")
                break
            except Exception as e:
                logger.error(f"处理消息时发生错误: {str(e)}")
                await asyncio.sleep(1)  # 发生错误时暂停1秒

    except Exception as e:
        logger.error(f"消息队列服务发生错误: {str(e)}")
    finally:
        # 清理资源
        if redis:
            await redis.aclose()
        await pool.aclose()
        logger.info("消息队列服务已关闭")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {str(e)}")
