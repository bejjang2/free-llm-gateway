import { useQuery } from '@tanstack/react-query'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { dashboardApi } from '@/lib/api'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { PageHeader } from '@/components/page-header'

export default function AnalyticsPage() {
  const { data: analytics } = useQuery({
    queryKey: ['analytics'],
    queryFn: () => dashboardApi.getAnalytics(),
    refetchInterval: 30000,
  })

  return (
    <div>
      <PageHeader title="Analytics" description="Usage across all providers." />

      <div className="space-y-6">
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {[
            { label: 'Requests', value: analytics?.total_requests ?? 0 },
            { label: 'Input tokens', value: formatTokens(analytics?.total_input_tokens) },
            { label: 'Output tokens', value: formatTokens(analytics?.total_output_tokens) },
          ].map(s => (
            <div key={s.label} className="rounded-lg border bg-card px-4 py-3">
              <p className="text-[11px] text-muted-foreground uppercase">{s.label}</p>
              <p className="text-xl font-semibold tabular-nums mt-1">{s.value}</p>
            </div>
          ))}
        </div>

        <div className="rounded-lg border bg-card">
          <div className="px-4 py-3 border-b"><h3 className="text-sm font-medium">Requests by provider</h3></div>
          <div className="p-4">
            {!analytics?.by_provider?.length ? (
              <p className="text-sm text-muted-foreground text-center py-8">No data yet</p>
            ) : (
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={analytics.by_provider}>
                  <CartesianGrid strokeDasharray="2 4" stroke="var(--border)" />
                  <XAxis dataKey="provider" tick={{ fontSize: 11 }} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="requests" fill="var(--foreground)" radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {analytics?.recent?.length ? (
          <div className="rounded-lg border bg-card">
            <div className="px-4 py-3 border-b"><h3 className="text-sm font-medium">Recent requests</h3></div>
            <div className="max-h-[360px] overflow-y-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Provider</TableHead>
                    <TableHead>Model</TableHead>
                    <TableHead className="text-right">In</TableHead>
                    <TableHead className="text-right">Out</TableHead>
                    <TableHead className="text-right">Latency</TableHead>
                    <TableHead>Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {analytics.recent.map((r, i) => (
                    <TableRow key={i}>
                      <TableCell className="text-xs">{r.provider}</TableCell>
                      <TableCell className="text-xs text-muted-foreground">{r.model}</TableCell>
                      <TableCell className="text-right tabular-nums">{formatTokens(r.input_tokens)}</TableCell>
                      <TableCell className="text-right tabular-nums">{formatTokens(r.output_tokens)}</TableCell>
                      <TableCell className="text-right tabular-nums">{r.latency_ms}ms</TableCell>
                      <TableCell className={r.success ? 'text-emerald-500' : 'text-rose-500'}>{r.success ? 'OK' : 'FAIL'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  )
}

function formatTokens(n?: number): string {
  if (!n) return '0'
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
  return String(n)
}
