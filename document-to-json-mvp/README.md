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

### OCR 페일백 사용
- 이미지 기반 문서까지 처리하려면 `brew install tesseract tesseract-lang` 후 `export TESSERACT_CMD=/opt/homebrew/bin/tesseract` 등으로 경로를 지정하세요.
- 서버 실행 전에 `export TOKKI_ENABLE_OCR=1`, `export TOKKI_OCR_LANGS=kor+eng` (필요 시 `TOKKI_OCR_CONFIG="--oem 3 --psm 6"`) 등을 설정하면 PDF/DOCX에 포함된 이미지 텍스트도 추출됩니다.
