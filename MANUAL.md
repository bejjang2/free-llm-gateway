# Free LLM Gateway 사용 설명서

## 1. 프로젝트 개요
13개 LLM Provider를 하나의 API로 통합하는 게이트웨이

### 지원 Provider
NVIDIA NIM, OpenRouter, Ollama, DeepSeek, Groq, Together AI, Cerebras, SambaNova, Mistral, GitHub Models, Zhipu, Gemini, LM Studio

### 주요 기능
- Auto-Failover: Provider 실패 시 자동 전환
- Web UI: API 키 관리, Failover 설정, 사용량 분석
- Unified API: Anthropic/OpenAI 호환

## 2. 설치

git clone https://github.com/bejjang2/free-llm-gateway.git
cd free-llm-gateway
uv sync
cd client && npm install && cd ..
cp .env.example .env

## 3. API Key 설정

.env 파일에 아래 항목 설정:
NVIDIA_NIM_API_KEY, OPENROUTER_API_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY, TOGETHER_API_KEY, CEREBRAS_API_KEY, SAMBANOVA_API_KEY, MISTRAL_API_KEY, GITHUB_API_KEY, ZHIPU_API_KEY, GEMINI_API_KEY

Local Provider:
OLLAMA_BASE_URL="http://localhost:11434/v1"
LM_STUDIO_BASE_URL="http://localhost:1234/v1"

Failover 설정:
FAILOVER_ENABLED=true
FAILOVER_PRIORITY="open_router,deepseek,groq,nvidia_nim"

## 4. 서버 실행

Backend:
uv run python server.py
-> http://localhost:8082

Web UI:
cd client && npm run dev
-> http://localhost:5173

## 5. API 사용법

Anthropic API:
curl -X POST http://localhost:8082/v1/messages -H "x-api-key: your-key" -H "Content-Type: application/json" -d {"model": "claude-3-5-sonnet-20241022", "max_tokens": 1024, "messages": [{"role": "user", "content": "안녕하세요!"}]}

OpenAI API:
curl -X POST http://localhost:8082/v1/chat/completions -H "Authorization: Bearer your-key" -H "Content-Type: application/json" -d {"model": "gpt-4", "messages": [{"role": "user", "content": "안녕하세요!"}]}

## 6. 문제 해결

서버 시작 안 됨: lsof -i :8082
401 오류: .env API Key 확인
Rate Limit: FAILOVER_PRIORITY에 대안 추가
Ollama 연결 안 됨: sudo ufw allow 11434
