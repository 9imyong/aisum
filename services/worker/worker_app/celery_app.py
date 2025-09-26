import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
RESULT_DB = os.getenv("CELERY_RESULT_DB_URI")  # db+mysql+pymysql://...

celery_app = Celery("worker_app")
celery_app.conf.update(
    broker_url=REDIS_URL,
    result_backend=RESULT_DB,  # 결과를 MySQL에 저장 (celery 결과 테이블 자동 생성)
    task_routes={
        "worker_app.tasks.*": {"queue": "celery"},
    },
    timezone="Asia/Seoul",
    enable_utc=True,
)

# Beat 스케줄 예시 (1분마다 더미 태스크)
celery_app.conf.beat_schedule = {
    "heartbeat-every-60s": {
        "task": "worker_app.tasks.heartbeat",
        "schedule": 60.0,
    }
}
