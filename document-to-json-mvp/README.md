# Document-to-JSON MVP Workspace

This folder contains the source code for the Document-to-JSON Converter proof of concept described in `PRD.md`.

## Structure
- `backend/` — FastAPI 서비스 (업로드 처리 및 JSON 변환 로직).
- `frontend/` — Next.js 웹 클라이언트 (업로드 UI, 프리뷰, 다운로드).
- `data/samples/` — 테스트용 문서 및 기대 JSON 결과.

Follow `../AGENTS.md` and `../TASK.md` for contributor guidelines and the active work queue.

## 실행 방법
1. 백엔드
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   # 루트에서 실행하려면: cd .. && uvicorn backend.main:app --reload
   uvicorn main:app --reload
   ```
2. 프론트엔드
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. 브라우저에서 `http://localhost:3000` 접속 후 문서를 업로드하여 JSON 결과를 확인합니다.
