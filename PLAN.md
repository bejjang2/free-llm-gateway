# free-claude-code + freellmapi Migration Plan

## Purpose
Integrate free-claude-code + freellmapi for CLI + Web UI Multi-provider API Gateway

## Phase 2: Backend
- api/auth.py : Unified key manager
- api/database.py : SQLite setup
- New endpoints: /v1/models, /dashboard/*

## Phase 3: Frontend Migration (from freellmapi)
- PlaygroundPage.tsx : Chat UI
- KeysPage.tsx : API key CRUD
- FallbackPage.tsx : Failover chain editor
- AnalyticsPage.tsx : Usage dashboard

## Phase 4: Database (SQLite)
- api_keys : encrypted provider keys
- usage_log : per-key usage tracking
- fallback_chain : failover priority

## Phase 5: Implementation Order
1. Backend: auth.py, database.py, routes.py (2 days)
2. Frontend: client/ setup, 4 pages (3 days)
3. Integration: CORS, Docker (2 days)
4. Deploy: README, GitHub push

## Estimated Time: 7 days

## Decision Points
1. Unified key system from freellmapi?
2. Provider pool merge?
3. Anthropic + OpenAI API format?
4. freellmapi dark mode style?

## References
- free-claude-code: https://github.com/Rishurajgautam24/free-claude-code
- freellmapi: https://github.com/tashfeenahmed/freellmapi
