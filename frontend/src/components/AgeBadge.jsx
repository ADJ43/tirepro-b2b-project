const AGE_CONFIG = {
  fresh:    { label: 'Fresh',    bg: 'bg-green-100',  text: 'text-green-800',  border: 'border-green-300' },
  normal:   { label: 'Normal',   bg: 'bg-blue-100',   text: 'text-blue-800',   border: 'border-blue-300' },
  aging:    { label: 'Aging',    bg: 'bg-yellow-100', text: 'text-yellow-800', border: 'border-yellow-300' },
  old:      { label: 'Old Stock', bg: 'bg-orange-100', text: 'text-orange-800', border: 'border-orange-300' },
  critical: { label: 'Critical', bg: 'bg-red-100',    text: 'text-red-800',    border: 'border-red-300' },
}

export default function AgeBadge({ ageCategory, dotCode, discountPercent, size = 'sm' }) {
  const config = AGE_CONFIG[ageCategory] || AGE_CONFIG.fresh

  const sizeClasses = size === 'sm'
    ? 'text-xs px-2 py-0.5'
    : 'text-sm px-3 py-1'

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full border font-medium ${config.bg} ${config.text} ${config.border} ${sizeClasses}`}
      title={dotCode ? `DOT: ${dotCode} — Manufactured week ${dotCode.slice(0,2)}, 20${dotCode.slice(2,4)}` : ''}
    >
      {config.label}
      {discountPercent > 0 && (
        <span className="font-bold">-{discountPercent}%</span>
      )}
    </span>
  )
}

export function AgeLegend() {
  return (
    <div className="flex flex-wrap gap-2 text-xs">
      {Object.entries(AGE_CONFIG).map(([key, cfg]) => (
        <span
          key={key}
          className={`inline-flex items-center rounded-full border px-2 py-0.5 ${cfg.bg} ${cfg.text} ${cfg.border}`}
        >
          {cfg.label}
        </span>
      ))}
    </div>
  )
}
