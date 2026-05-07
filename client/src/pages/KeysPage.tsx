import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { dashboardApi } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { PageHeader } from '@/components/page-header'

const PLATFORMS = [
  { value: 'nvidia_nim', label: 'NVIDIA NIM' },
  { value: 'open_router', label: 'OpenRouter' },
  { value: 'groq', label: 'Groq' },
  { value: 'cerebras', label: 'Cerebras' },
  { value: 'sambanova', label: 'SambaNova' },
  { value: 'mistral', label: 'Mistral' },
  { value: 'deepseek', label: 'DeepSeek' },
  { value: 'together', label: 'Together AI' },
  { value: 'github', label: 'GitHub Models' },
  { value: 'zhipu', label: 'Zhipu AI' },
  { value: 'lmstudio', label: 'LM Studio (local)' },
  { value: 'ollama', label: 'Ollama (local)' },
]

export default function KeysPage() {
  const queryClient = useQueryClient()
  const [platform, setPlatform] = useState('')
  const [apiKey, setApiKey] = useState('')
  const [label, setLabel] = useState('')

  const { data: keysData, isLoading } = useQuery({
    queryKey: ['keys'],
    queryFn: () => dashboardApi.getKeys(),
    refetchInterval: 30000,
  })

  const addKey = useMutation({
    mutationFn: (body: { provider: string; provider_key: string; label?: string }) =>
      dashboardApi.addKey(body.provider, body.provider_key, body.label),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['keys'] })
      setPlatform('')
      setApiKey('')
      setLabel('')
    },
  })

  const deleteKey = useMutation({
    mutationFn: (id: string) => dashboardApi.deleteKey(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['keys'] }),
  })

  const keys = keysData?.keys ?? []
  const grouped = PLATFORMS.map(p => ({
    ...p,
    keys: keys.filter(k => k.provider === p.value),
  })).filter(p => p.keys.length > 0)

  return (
    <div>
      <PageHeader
        title="Keys"
        description="Manage provider API keys. Keys are AES-256-GCM encrypted at rest."
      />

      <div className="space-y-8">
        <section>
          <h2 className="text-sm font-medium mb-3">Add a provider key</h2>
          <form
            onSubmit={e => { e.preventDefault(); if (platform && apiKey) addKey.mutate({ provider: platform, provider_key: apiKey, label }) }}
            className="flex flex-wrap items-end gap-3 rounded-lg border p-4 bg-card"
          >
            <div className="space-y-1.5">
              <Label className="text-xs">Platform</Label>
              <Select value={platform} onValueChange={(v) => setPlatform(v ?? "")}>
                <SelectTrigger className="w-[220px]">
                  <SelectValue placeholder="Select provider" />
                </SelectTrigger>
                <SelectContent>
                  {PLATFORMS.map(p => (
                    <SelectItem key={p.value} value={p.value}>{p.label}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5 flex-1 min-w-[240px]">
              <Label className="text-xs">API Key</Label>
              <Input type="password" value={apiKey} onChange={e => setApiKey(e.target.value)} placeholder="paste your API key" className="font-mono text-xs" />
            </div>
            <div className="space-y-1.5">
              <Label className="text-xs">Label</Label>
              <Input value={label} onChange={e => setLabel(e.target.value)} placeholder="optional" className="w-[160px]" />
            </div>
            <Button type="submit" size="sm" disabled={!platform || !apiKey || addKey.isPending}>
              {addKey.isPending ? 'Adding...' : 'Add key'}
            </Button>
          </form>
        </section>

        <section>
          <h2 className="text-sm font-medium mb-3">Saved keys ({keys.length})</h2>
          {isLoading ? (
            <p className="text-sm text-muted-foreground">Loading...</p>
          ) : grouped.length === 0 ? (
            <div className="rounded-lg border border-dashed p-8 text-center">
              <p className="text-sm text-muted-foreground">No keys saved yet. Add one above.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {grouped.map(group => (
                <div key={group.value}>
                  <h3 className="text-sm font-medium mb-2">{group.label} ({group.keys.length})</h3>
                  <div className="rounded-lg border divide-y bg-card overflow-hidden">
                    {group.keys.map(k => (
                      <div key={k.id} className="flex items-center gap-3 px-4 py-3 hover:bg-muted/40">
                        <span className="size-1.5 rounded-full bg-emerald-500" />
                        <code className="text-xs font-mono">{k.id}</code>
                        {k.label && <span className="text-xs text-muted-foreground">{k.label}</span>}
                        <div className="flex-1" />
                        <span className="text-[11px] text-muted-foreground">{new Date(k.created_at).toLocaleDateString()}</span>
                        <Button variant="ghost" size="xs" className="text-muted-foreground hover:text-destructive" onClick={() => deleteKey.mutate(k.id)}>Remove</Button>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  )
}
