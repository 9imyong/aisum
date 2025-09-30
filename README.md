이벤트/비동기 미니 마이크로서비스

스택: FastAPI + Kafka(KRaft) + aiokafka Consumer + Celery(브로커: Redis) + MySQL + Adminer
한 줄 설명: “요청은 빨리 받고, 무거운 일은 뒤로 넘기는” 이벤트/비동기 중심 서비스 예제

이 프로젝트는 API 서버가 사용자 요청을 즉시 수락(빠른 응답) 하고, 시간이 오래 걸리는 작업은 메시지 큐로 위임하여 백그라운드에서 처리하는 마이크로서비스 아키텍처의 최소 구현체입니다.

Client
  │  POST /submit {"text": "..."}
  ▼
FastAPI (api)
  ├─ MySQL에 Job 레코드 생성(QUEUED)
  └─ Kafka "jobs" 토픽으로 이벤트 발행
        ▼
   aiokafka Consumer
        └─ Celery 태스크 enqueue (브로커: Redis)
              ▼
           Celery Worker
              ├─ (예시) aiohttp로 외부 API 호출
              └─ 처리 결과를 MySQL에 업데이트 (DONE/FAILED)

조회: GET /results/{id} → MySQL에서 현재 상태/노트 조회

서비스 구성

api (FastAPI): 요청 수신, DB 기록, Kafka 발행 (:8000)

kafka (KRaft 모드): 이벤트 스트림 브로커 (kafka:9092) — Zookeeper 불필요

consumer (aiokafka): Kafka 구독 → Celery 태스크로 전달

worker (Celery): 비동기 작업 실행(예: 외부 API 호출) 후 DB 업데이트

beat (Celery Beat, 선택): 주기작업 스케줄링(예: heartbeat)

mysql: 영속 데이터 저장 (:3306)

adminer: DB 웹 콘솔 (:8080)

redis: Celery 브로커(큐)

트러블슈팅(요약)
**API가 DB 연결 실패
- MySQL 시작 대기(healthcheck) + init_db()에 재시도(backoff) 권장
.env의 SQLALCHEMY_DB_URI 확인
- consumer가 Kafka에 못 붙음
ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092 확인
- Kafka healthcheck + consumer.depends_on + restart 설정
run_consumer.py에 부트스트랩 재시도 코드 추가
- Celery 태스크 “unregistered”
services/worker/worker_app/__init__.py 파일 추가
celery_app.py 하단에 from . import tasks 추가
- PyMySQL 인증 에러 (caching_sha2_password)
cryptography 패키지 설치(권장) 또는 MySQL 유저를 mysql_native_password로 변경**

## 디렉터리 구조

```
quikqueue/
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
