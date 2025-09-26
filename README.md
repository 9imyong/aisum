## 디렉터리 구조

```
aisum/
├── docker-compose.yml
├── .env
├── README.md
├── services
│   ├── api
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app
│   │       ├── main.py
│   │       ├── db.py
│   │       ├── models.py
│   │       └── kafka_producer.py
│   ├── consumer
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── run_consumer.py
│   └── worker
│       ├── Dockerfile
│       ├── requirements.txt
│       └── worker_app
│           ├── celery_app.py
│           ├── tasks.py
│           ├── db.py
│           └── models.py
```
