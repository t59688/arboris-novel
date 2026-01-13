# AIMETA P=Celery配置_异步任务队列设置|R=Celery应用_任务路由_序列化|NR=不含任务定义|E=celery_app|X=job|A=Celery实例|D=celery,redis|S=net|RD=./README.ai
import os
from celery import Celery
from kombu import Exchange, Queue
from dotenv import load_dotenv

load_dotenv()

# 创建 Celery 应用
app = Celery(
    'arboris',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1'),
)

# Celery 配置
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 分钟
    task_soft_time_limit=25 * 60,  # 25 分钟
    result_expires=3600,  # 结果保留 1 小时
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# 定义任务队列
app.conf.task_queues = (
    Queue('emotion_analysis', Exchange('emotion_analysis'), routing_key='emotion_analysis'),
    Queue('default', Exchange('default'), routing_key='default'),
)

# 定义任务路由
app.conf.task_routes = {
    'app.tasks.emotion_tasks.analyze_emotion_async': {'queue': 'emotion_analysis'},
}

# 定义定时任务（可选）
app.conf.beat_schedule = {
    # 可以在这里添加定时任务
}

if __name__ == '__main__':
    app.start()
