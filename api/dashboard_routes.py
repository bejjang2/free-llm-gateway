"""Dashboard API endpoints for Web UI."""

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.database import get_connection
from api.auth import get_key_manager
from config.settings import get_settings

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class AddKeyRequest(BaseModel):
    provider: str
    provider_key: str
    label: str = ""

class UpdateFallbackRequest(BaseModel):
    chains: list[dict]


@router.get("/status")
async def dashboard_status():
    settings = get_settings()
    conn = get_connection()
    rows = conn.execute("SELECT provider, is_active FROM api_keys").fetchall()
    conn.close()
    providers = {
        "nvidia_nim": bool(settings.nvidia_nim_api_key),
        "open_router": bool(settings.open_router_api_key),
        "deepseek": bool(settings.deepseek_api_key),
        "groq": bool(settings.groq_api_key),
        "together": bool(settings.together_api_key),
        "cerebras": bool(settings.cerebras_api_key),
        "sambanova": bool(settings.sambanova_api_key),
        "mistral": bool(settings.mistral_api_key),
        "github": bool(settings.github_api_key),
        "zhipu": bool(settings.zhipu_api_key),
        "ollama": True, "lmstudio": True,
    }
    return {"status": "ok", "provider": settings.provider_type, "providers": providers}


@router.get("/keys")
async def list_keys():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, provider, label, created_at, is_active FROM api_keys ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return {"keys": [{"id": r["id"], "provider": r["provider"],
        "label": r["label"], "created_at": r["created_at"],
        "is_active": bool(r["is_active"])} for r in rows]}


@router.post("/keys")
async def add_key(req: AddKeyRequest):
    km = get_key_manager()
    conn = get_connection()
    key_id = f"key_{uuid.uuid4().hex[:12]}"
    encrypted = km.encrypt_provider_key(req.provider_key)
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO api_keys (id, key_hash, encrypted_key, provider, label, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (key_id, key_id, encrypted, req.provider, req.label, now, now))
    conn.commit()
    conn.close()
    return {"status": "ok", "id": key_id}


@router.delete("/keys/{key_id}")
async def delete_key(key_id: str):
    conn = get_connection()
    conn.execute("DELETE FROM api_keys WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}


@router.get("/fallback-chain")
async def get_fallback_chain():
    conn = get_connection()
    rows = conn.execute("SELECT provider, priority, max_retries, is_active FROM fallback_chain ORDER BY priority").fetchall()
    conn.close()
    return {"chains": [dict(r) for r in rows]}


@router.put("/fallback-chain")
async def update_fallback_chain(req: UpdateFallbackRequest):
    conn = get_connection()
    conn.execute("DELETE FROM fallback_chain")
    for c in req.chains:
        conn.execute("INSERT INTO fallback_chain (provider, priority, max_retries, is_active) VALUES (?, ?, ?, ?)",
            (c["provider"], c["priority"], c.get("max_retries", 2), int(c.get("is_active", True))))
    conn.commit()
    conn.close()
    return {"status": "updated"}


@router.get("/analytics")
async def get_analytics():
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) as cnt, SUM(input_tokens) as inp, SUM(output_tokens) as out FROM usage_log").fetchone()
    by_provider = conn.execute("SELECT provider, COUNT(*) as cnt FROM usage_log GROUP BY provider ORDER BY cnt DESC LIMIT 20").fetchall()
    recent = conn.execute("SELECT provider, model, input_tokens, output_tokens, latency_ms, success, created_at FROM usage_log ORDER BY created_at DESC LIMIT 50").fetchall()
    conn.close()
    return {"total_requests": total["cnt"] or 0, "total_input_tokens": total["inp"] or 0,
        "total_output_tokens": total["out"] or 0,
        "by_provider": [dict(r) for r in by_provider],
        "recent": [dict(r) for r in recent]}


@router.get("/models")
async def list_models():
    settings = get_settings()
    models = {
        "nvidia_nim": ["meta/llama3-70b", "z-ai/glm4.7", "moonshotai/kimi-k2"],
        "open_router": ["deepseek/deepseek-r1:free", "openai/gpt-oss-120b:free"],
        "deepseek": ["deepseek-chat", "deepseek-reasoner"],
        "groq": ["llama-3.3-70b", "qwen-3-30b"],
        "together": ["Llama-3.3-70B", "DeepSeek-V3"],
        "cerebras": ["llama-3.3-70b"],
        "sambanova": ["Llama-4-Maverick", "DeepSeek-V3"],
        "mistral": ["mistral-large", "codestral"],
        "github": ["gpt-4o", "gpt-4.1"],
        "zhipu": ["glm-4-flash", "glm-4-plus"],
        "ollama": ["llama3.2", "qwen2.5"],
        "lmstudio": ["local-model"],
    }
    return {"providers": {k: {"models": v} for k, v in models.items()}}
