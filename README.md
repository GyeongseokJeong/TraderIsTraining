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

### 1. PostgreSQL 시작

```bash
docker compose up -d postgres
```

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

백엔드 기본 주소는 `http://localhost:8000` 입니다.

### 3. 프론트엔드 설정

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

프론트엔드 기본 주소는 `http://localhost:5173` 입니다.

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

- `DATABASE_URL`: PostgreSQL 접속 문자열
- `CORS_ORIGINS`: 허용할 프론트엔드 origin 목록
- `VITE_API_BASE_URL`: 프론트엔드에서 호출할 백엔드 API base URL

## 데이터 동작 주의사항

Upbit는 거래가 없는 구간의 캔들을 생성하지 않을 수 있습니다. MVP에서는 없는 캔들을 임의로 보간하지 않고 Upbit가 제공한 실제 캔들만 저장하고 재생합니다.

## 보안/안전 원칙

- 브라우저에서 Upbit를 직접 호출하지 않습니다.
- Upbit API 키를 요구하거나 저장하지 않습니다.
- 실제 주문 API 또는 거래소 계정 연동을 구현하지 않습니다.
- 활성 세션에서는 서버가 현재 replay index까지만 캔들을 반환합니다.
