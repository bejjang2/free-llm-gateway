import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  DndContext, closestCenter, KeyboardSensor, PointerSensor,
  useSensor, useSensors, type DragEndEvent,
} from '@dnd-kit/core'
import {
  arrayMove, SortableContext, sortableKeyboardCoordinates,
  useSortable, verticalListSortingStrategy,
} from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { dashboardApi, type FallbackChain } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { PageHeader } from '@/components/page-header'

function SortableRow({ entry, index, onToggle }: { entry: FallbackChain; index: number; onToggle: (prov: string, enabled: boolean) => void }) {
  const { attributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: entry.provider })
  return (
    <div ref={setNodeRef} style={{ transform: CSS.Transform.toString(transform), transition }}
      className={`group flex items-center gap-3 px-4 py-3 bg-card ${isDragging ? 'opacity-50' : ''} ${entry.is_active ? '' : 'opacity-50'}`}>
      <button {...attributes} {...listeners} className="cursor-grab text-muted-foreground/50 hover:text-foreground" aria-label="Drag to reorder">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
          <circle cx="9" cy="6" r="1.5" /><circle cx="15" cy="6" r="1.5" />
          <circle cx="9" cy="12" r="1.5" /><circle cx="15" cy="12" r="1.5" />
          <circle cx="9" cy="18" r="1.5" /><circle cx="15" cy="18" r="1.5" />
        </svg>
      </button>
      <span className="text-xs font-mono text-muted-foreground w-5 tabular-nums">{index + 1}</span>
      <div className="flex-1">
        <span className="font-medium text-sm">{entry.provider}</span>
        <span className="text-xs text-muted-foreground ml-2">retries: {entry.max_retries}</span>
      </div>
      <Switch checked={entry.is_active} onCheckedChange={(checked) => onToggle(entry.provider, checked)} />
    </div>
  )
}

export default function FallbackPage() {
  const queryClient = useQueryClient()
  const [local, setLocal] = useState<FallbackChain[] | null>(null)

  const { data, isLoading } = useQuery({
    queryKey: ['fallback'],
    queryFn: async () => {
      const res = await dashboardApi.getFallbackChain()
      return res.chains
    },
  })

  const saveMutation = useMutation({
    mutationFn: (chains: FallbackChain[]) => dashboardApi.updateFallbackChain(chains),
    onSuccess: () => { queryClient.invalidateQueries({ queryKey: ['fallback'] }); setLocal(null) },
  })

  const entries = local ?? data ?? []

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates }),
  )

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event
    if (!over || active.id === over.id) return
    const oldIdx = entries.findIndex(e => e.provider === active.id)
    const newIdx = entries.findIndex(e => e.provider === over.id)
    const reordered = arrayMove(entries, oldIdx, newIdx).map((e, i) => ({ ...e, priority: i + 1 }))
    setLocal(reordered)
  }

  function handleToggle(provider: string, enabled: boolean) {
    setLocal(entries.map(e => e.provider === provider ? { ...e, is_active: enabled } : e))
  }

  return (
    <div>
      <PageHeader title="Fallback Chain" description="Drag to reorder. Requests try providers top-to-bottom until one succeeds."
        actions={local && (
          <>
            <Button variant="outline" size="sm" onClick={() => setLocal(null)}>Discard</Button>
            <Button size="sm" onClick={() => saveMutation.mutate(entries)}>Save order</Button>
          </>
        )}
      />
      {isLoading ? <p className="text-sm text-muted-foreground">Loading...</p> : entries.length === 0 ? (
        <div className="rounded-lg border border-dashed p-8 text-center">
          <p className="text-sm text-muted-foreground">No fallback chain configured. Add keys first.</p>
        </div>
      ) : (
        <div className="rounded-lg border divide-y overflow-hidden">
          <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
            <SortableContext items={entries.map(e => e.provider)} strategy={verticalListSortingStrategy}>
              {entries.map((e, i) => <SortableRow key={e.provider} entry={e} index={i} onToggle={handleToggle} />)}
            </SortableContext>
          </DndContext>
        </div>
      )}
    </div>
  )
}
