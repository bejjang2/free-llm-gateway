const BASE = import.meta.env.BASE_URL.replace(/\/$/, '');

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({ error: { message: res.statusText } }));
    throw new Error(body.error?.message ?? `HTTP ${res.status}`);
  }
  return res.json();
}

// --- Dashboard API ---
export interface ProviderStatus {
  provider: string;
  is_active: boolean;
}

export interface DashboardStatus {
  status: string;
  provider: string;
  providers: Record<string, boolean>;
  saved_keys: number;
}

export interface KeyInfo {
  id: string;
  provider: string;
  label: string;
  created_at: string;
  is_active: boolean;
}

export interface FallbackChain {
  provider: string;
  priority: number;
  max_retries: number;
  is_active: boolean;
}

export interface AnalyticsData {
  total_requests: number;
  total_input_tokens: number;
  total_output_tokens: number;
  by_provider: Array<{
    provider: string;
    requests: number;
    input_tokens: number;
    output_tokens: number;
    avg_latency_ms: number;
  }>;
  recent: Array<{
    provider: string;
    model: string;
    input_tokens: number;
    output_tokens: number;
    latency_ms: number;
    success: boolean;
    created_at: string;
  }>;
}

export interface ModelProvider {
  models: string[];
  has_key?: boolean;
}

export const dashboardApi = {
  getStatus: () => apiFetch<DashboardStatus>('/dashboard/status'),
  
  getKeys: () => apiFetch<{ keys: KeyInfo[] }>('/dashboard/keys'),
  addKey: (provider: string, provider_key: string, label?: string) =>
    apiFetch<{ status: string; id: string }>('/dashboard/keys', {
      method: 'POST',
      body: JSON.stringify({ provider, provider_key, label }),
    }),
  deleteKey: (keyId: string) =>
    apiFetch<{ status: string }>(`/dashboard/keys/${keyId}`, { method: 'DELETE' }),

  getFallbackChain: () =>
    apiFetch<{ chains: FallbackChain[] }>('/dashboard/fallback-chain'),
  updateFallbackChain: (chains: FallbackChain[]) =>
    apiFetch<{ status: string }>('/dashboard/fallback-chain', {
      method: 'PUT',
      body: JSON.stringify({ chains }),
    }),

  getAnalytics: () => apiFetch<AnalyticsData>('/dashboard/analytics'),
  getModels: () =>
    apiFetch<{ providers: Record<string, ModelProvider> }>('/dashboard/models'),
};
