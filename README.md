# Trader Is Training

Trader Is Training은 Upbit KRW 마켓의 과거 캔들을 한 캔들씩 재생하면서 가상 매매를 연습하고, 세션 종료 후 전체 차트에서 매매 결정을 복기하는 학습용 도구입니다.

> 이 서비스는 학습용 가상 트레이딩 도구이며 실제 투자 조언이나 실제 주문 기능을 제공하지 않습니다.

## 구성

- `backend/`: FastAPI, SQLAlchemy, Alembic, PostgreSQL 기반 API 서버
- `frontend/`: React, TypeScript, Vite, TanStack Query, lightweight-charts 기반 웹 앱
- `docker-compose.yml`: 로컬 PostgreSQL 실행

## 주요 기능

- KRW-BTC, KRW-ETH, KRW-XRP, KRW-SOL 마켓 지원 구조
- 1분, 5분, 15분, 60분, 240분, 일봉 타임프레임 지원 구조
- Upbit public quotation candle API 서버 사이드 연동
- PostgreSQL 캔들 캐시
- 활성 트레이닝 세션에서 현재 replay index까지만 캔들 반환
- 매수/매도/관망/다음 캔들/세션 종료
- 수수료 반영 가상 체결
- 거래 내역과 equity snapshot 저장
- 세션 종료 후 전체 캔들, 거래 마커, 성과 지표 복기

## 로컬 실행

로컬 단독 실행에서는 기본 포트를 그대로 사용할 수 있습니다. 같은 머신에서 JAsset 등 다른 서비스와 함께 실행한다면 [EC2에서 JAsset과 함께 실행](#ec2에서-jasset과-함께-실행)을 먼저 확인하세요.

### 1. PostgreSQL 시작

```bash
cp .env.example .env
docker compose up -d postgres
```

기본 예시는 호스트 PostgreSQL 포트로 `55432`를 사용합니다. 다른 포트를 사용하려면 루트 `.env`의 `POSTGRES_HOST_PORT`와 `DATABASE_URL` 포트를 같은 값으로 변경하세요.

### 2. 백엔드 설정

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp ../.env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

백엔드 기본 주소는 `http://localhost:8000` 입니다. 루트 `.env.example`의 공존 실행 예시를 그대로 사용한다면 `backend/.env`의 `DATABASE_URL` 포트가 PostgreSQL 호스트 포트 `55432`를 바라봅니다.

### 3. 프론트엔드 설정

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

프론트엔드 기본 주소는 `http://localhost:5173` 입니다. 로컬 기본 포트로 실행하려면 `frontend/.env`의 `VITE_API_BASE_URL`을 `http://localhost:8000/api`로 맞추세요.


## 통합 서버 실행 스크립트

JAsset과 동일하게 한 번의 명령으로 PostgreSQL, 백엔드, 프론트엔드 개발 서버를 함께 구동할 수 있는 스크립트를 제공합니다. 스크립트는 필요한 `.env` 파일이 없을 때 예시 파일로 생성하고, PostgreSQL 시작, 백엔드 의존성 설치, Alembic 마이그레이션, 프론트엔드 의존성 설치 후 서버를 실행합니다.

```bash
./utils/run_server.sh
```

기본 포트는 JAsset과 함께 실행하기 위한 공존 예시 값인 백엔드 `18000`, 프론트엔드 `15173`을 사용합니다. 스크립트는 실행 시 `CORS_ORIGINS`와 `VITE_API_BASE_URL` 기본값도 해당 포트에 맞춰 주며, 포트를 바꿔야 한다면 환경 변수로 덮어쓸 수 있습니다.

```bash
BACKEND_PORT=18001 FRONTEND_PORT=15174 ./utils/run_server.sh
```

스크립트 실행 전 루트 `.env`, `backend/.env`, `frontend/.env`를 직접 만들어 둔 경우 기존 파일은 덮어쓰지 않습니다. 외부 공개 환경에서는 `CORS_ORIGINS`와 `VITE_API_BASE_URL`이 실제 접속 주소를 가리키도록 확인하세요. `CORS_ORIGINS` 예시는 JSON 배열 형식을 사용하지만, 여러 origin을 쉼표로 구분한 문자열도 지원합니다. shell에서 직접 `export CORS_ORIGINS=...`를 실행할 때는 JSON 배열 내부 따옴표가 shell 처리로 제거되지 않도록 전체 값을 작은따옴표로 감싸세요.

## EC2에서 JAsset과 함께 실행

JAsset과 같은 EC2에서 구동할 때는 포트, DB 접속 문자열, CORS origin, 프론트엔드 API 주소를 Trader Is Training 전용 값으로 분리해야 합니다. 아래 값은 예시이며, EC2에서 이미 사용 중인 포트와 겹치면 반드시 다른 값으로 변경하세요.

| 구성 요소 | 권장 예시 | 충돌 시 변경 위치 |
| --- | --- | --- |
| PostgreSQL 호스트 포트 | `55432` | 루트 `.env`의 `POSTGRES_HOST_PORT`, `DATABASE_URL` |
| 백엔드 포트 | `18000` | 백엔드 실행 명령, 루트 `.env`의 `CORS_ORIGINS`, `frontend/.env`의 `VITE_API_BASE_URL` |
| 프론트엔드 포트 | `15173` | 프론트엔드 실행 명령, 루트 `.env`의 `CORS_ORIGINS` |

### 1. 루트 환경 변수 설정

```bash
cp .env.example .env
```

EC2에서 외부 접속을 허용해야 한다면 `<EC2_PUBLIC_IP>`를 실제 EC2 퍼블릭 IP 또는 도메인으로 변경하세요.

```dotenv
POSTGRES_HOST_PORT=55432
DATABASE_URL=postgresql+psycopg://trader:trader@localhost:55432/trader_is_training
CORS_ORIGINS=["http://<EC2_PUBLIC_IP>:15173"]
```

shell에서 직접 export하는 경우에는 `export CORS_ORIGINS='["http://<EC2_PUBLIC_IP>:15173"]'`처럼 전체 JSON 배열 문자열을 작은따옴표로 감싸세요.

`POSTGRES_HOST_PORT`와 `DATABASE_URL` 안의 포트는 반드시 일치해야 합니다. 예를 들어 `POSTGRES_HOST_PORT=55433`으로 변경했다면 `DATABASE_URL`도 `localhost:55433`으로 변경해야 합니다.

### 2. PostgreSQL 시작

```bash
docker compose up -d postgres
```

포트 충돌이 있는지 확인하려면 다음 명령을 사용할 수 있습니다.

```bash
docker compose ps postgres
```

### 3. 백엔드 실행

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp ../.env.example .env
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 18000
```

EC2 내부에서만 프록시를 통해 접근시킬 계획이라면 방화벽 또는 보안 그룹에서 `18000` 포트를 직접 공개하지 않아도 됩니다. 외부에서 직접 호출해야 한다면 EC2 보안 그룹에서 필요한 출발지에만 `18000` 포트를 허용하세요.

### 4. 프론트엔드 실행

```bash
cd frontend
cp .env.example .env
npm install
npm run dev -- --host 0.0.0.0 --port 15173
```

`frontend/.env`는 백엔드 주소를 바라보도록 설정합니다.

```dotenv
VITE_API_BASE_URL=http://<EC2_PUBLIC_IP>:18000/api
```

운영 환경에서는 Vite 개발 서버를 직접 공개하기보다 빌드 결과물을 Nginx 같은 리버스 프록시 또는 정적 파일 서버 뒤에서 제공하는 것을 권장합니다.

### 5. 공존 실행 체크리스트

- JAsset이 사용하는 포트와 `55432`, `18000`, `15173`이 겹치지 않는지 확인합니다.
- `POSTGRES_HOST_PORT`와 `DATABASE_URL` 포트가 같은지 확인합니다.
- `CORS_ORIGINS`에 실제 프론트엔드 origin이 포함되어 있는지 확인합니다.
- `VITE_API_BASE_URL`이 실제 백엔드 `/api` 주소를 바라보는지 확인합니다.
- EC2 보안 그룹은 필요한 포트와 필요한 출발지에만 열어 둡니다.
- 운영 배포에서는 HTTPS와 리버스 프록시 적용을 권장합니다.

## 테스트와 체크

### 백엔드

```bash
cd backend
python -m pytest app/tests
python -m ruff check app
```

### 프론트엔드

```bash
cd frontend
npm run typecheck
npm run build
```

## 환경 변수

백엔드는 루트 `.env.example`을 참고하고, 프론트엔드는 `frontend/.env.example`을 참고합니다:

- `POSTGRES_HOST_PORT`: Docker Compose PostgreSQL 호스트 포트
- `DATABASE_URL`: PostgreSQL 접속 문자열
- `CORS_ORIGINS`: 허용할 프론트엔드 origin 목록. JSON 배열 문자열 예: `["http://localhost:15173"]`; 쉼표 구분 문자열 예: `http://localhost:15173,http://127.0.0.1:15173`도 지원합니다. shell에서 직접 export할 때는 `export CORS_ORIGINS='["http://localhost:15173"]'`처럼 전체 값을 작은따옴표로 감싸세요.
- `VITE_API_BASE_URL`: 프론트엔드에서 호출할 백엔드 API base URL

## 데이터 동작 주의사항

Upbit는 거래가 없는 구간의 캔들을 생성하지 않을 수 있습니다. MVP에서는 없는 캔들을 임의로 보간하지 않고 Upbit가 제공한 실제 캔들만 저장하고 재생합니다.

## 보안/안전 원칙

- 브라우저에서 Upbit를 직접 호출하지 않습니다.
- Upbit API 키를 요구하거나 저장하지 않습니다.
- 실제 주문 API 또는 거래소 계정 연동을 구현하지 않습니다.
- 활성 세션에서는 서버가 현재 replay index까지만 캔들을 반환합니다.
- EC2에서 직접 포트를 공개할 때는 보안 그룹에서 필요한 출발지만 허용합니다.
- 운영 환경에서는 HTTPS와 리버스 프록시를 사용해 백엔드와 프론트엔드를 노출하는 것을 권장합니다.
