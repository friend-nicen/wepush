微信每天都要用，所以很多系统监控的消息就直接推送到微信了，这样有什么问题也能很方便的及时收到提醒。

但是呢，微信机器人现在封号太厉害了，用过wechaty，再到hook微信客户端，现在都是一挂就封，无奈了，只好走正规军的路子。

# WePush 微信消息推送系统

## 项目概述

WePush 是一个基于 [weauto](https://github.com/cluic/wxauto) 开发的微信消息推送系统，采用模拟人工点击的方式实现消息发送，具有安全稳定、零封号风险的特点。 系统通过 HTTP API 接收消息请求并利用消息队列异步处理微信消息的发送，完全模拟真实的人工操作，避免了微信封号风险。

## 技术架构

### 核心组件

- **FastAPI 服务器 (main.py)**
  - 提供 HTTP API 接口
  - 处理消息请求的接收和验证
  - 将消息存入 Redis 队列

- **消息队列处理器 (mq.py)**
  - 监听 Redis 队列
  - 处理消息发送任务
  - 集成微信自动化模块
  - 基于模拟点击技术，安全稳定
  - 完全模拟人工操作，零封号风险

### 依赖项目

- FastAPI：高性能的异步 Web 框架
- Redis：消息队列和数据存储
- wxauto：微信 Windows 客户端自动化模块
- uvicorn：ASGI 服务器

## 运行环境要求

- Python 3.12+
- Windows 操作系统
- Redis 服务器
- 微信 Windows 客户端

## 安装配置

1. 安装依赖包：
```bash
pip install -r requirements.txt
```

2. 确保 Redis 服务已启动且可访问（默认地址：redis://localhost）

3. 登录微信 Windows 客户端

## 启动服务

1. 启动消息接收服务器：
```bash
python main.py
```
服务器将在 http://localhost:8000 启动

2. 启动消息处理队列：
```bash
python mq.py
```

**重要：必须提前打开指定好友或群聊的聊天窗口（并且是在独立窗口打开），收到消息推送请求时会自动忽略未打开聊天窗口的目标！**

可以通过pyinstaller指定项目内的build.spec，将项目打包为exe可执行文件

```bash
pyinstaller build.spec
```

## API 接口文档

### 发送消息

- **接口**：`POST /api/sendMsg`
- **Content-Type**：`application/json`
- **请求参数**：
  ```json
  {
    "receiver": "群名或者好友昵称",
    "msg": "消息内容"
  }
  ```
- **响应格式**：
  ```json
  {
    "code": 1,
    "taskId": 123,
    "msg": "任务提交成功"
  }
  ```

## 常见问题

1. **Q: 消息发送失败怎么办？**
   A: 检查以下几点：
   - 确保微信客户端已登录
   - 验证接收人昵称/微信号是否正确
   - 检查 Redis 服务是否正常运行

2. **Q: 如何修改 Redis 连接配置？**
   A: 在 main.py 和 mq.py 中修改 redis_url 变量

## 注意事项

- 使用前请确保微信客户端已登录
- 为保证稳定性，建议保持微信窗口在前台运行

## 许可证

本项目基于 MIT 许可证开源