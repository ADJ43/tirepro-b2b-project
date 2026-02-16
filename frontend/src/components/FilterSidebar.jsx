import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
import AgeBadge from './AgeBadge'

function CollapsibleSection({ title, defaultOpen = true, children }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="mb-4">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center justify-between w-full text-sm font-medium text-gray-700 mb-2 hover:text-primary"
      >
        {title}
        <span className="text-xs">{open ? '▼' : '▶'}</span>
      </button>
      {open && children}
    </div>
  )
}

export default function FilterSidebar({ filters, onChange, search }) {
  // Build params for facets query (same filters as product list)
  const facetParams = {}
  if (search) facetParams.search = search
  if (filters.brand_id) facetParams.brand_id = filters.brand_id
  if (filters.category_id) facetParams.category_id = filters.category_id
  if (filters.min_price) facetParams.min_price = filters.min_price
  if (filters.max_price) facetParams.max_price = filters.max_price
  if (filters.in_stock) facetParams.in_stock = true
  if (filters.tire_size) facetParams.tire_size = filters.tire_size
  if (filters.tire_type) facetParams.tire_type = filters.tire_type

  const { data: facets } = useQuery({
    queryKey: ['facets', facetParams],
    queryFn: () => api.get('/products/facets', { params: facetParams }).then(r => r.data),
    keepPreviousData: true,
  })

  const update = (key, val) => onChange({ ...filters, [key]: val, page: 1 })

  return (
    <aside className="w-full lg:w-64 bg-white rounded-lg shadow p-5 h-fit lg:sticky lg:top-24 shrink-0">
      <h2 className="font-bold text-primary mb-4">Filters</h2>

      {/* Brand */}
      <CollapsibleSection title="Brand">
        <div className="space-y-1 max-h-48 overflow-y-auto">
          <button
            onClick={() => update('brand_id', null)}
            className={`block w-full text-left text-sm px-2 py-1 rounded ${!filters.brand_id ? 'bg-primary text-white' : 'hover:bg-gray-100'}`}
          >
            All Brands
          </button>
          {facets?.brands?.map(b => (
            <button
              key={b.id}
              onClick={() => update('brand_id', b.id)}
              className={`flex justify-between w-full text-left text-sm px-2 py-1 rounded ${
                Number(filters.brand_id) === b.id ? 'bg-primary text-white' : b.count === 0 ? 'text-gray-300' : 'hover:bg-gray-100'
              }`}
              disabled={b.count === 0}
            >
              <span>{b.name}</span>
              <span className={`text-xs ${Number(filters.brand_id) === b.id ? 'text-white/70' : 'text-gray-400'}`}>
                {b.count}
              </span>
            </button>
          ))}
        </div>
      </CollapsibleSection>

      {/* Category */}
      <CollapsibleSection title="Category">
        <div className="space-y-1 max-h-48 overflow-y-auto">
          <button
            onClick={() => update('category_id', null)}
            className={`block w-full text-left text-sm px-2 py-1 rounded ${!filters.category_id ? 'bg-primary text-white' : 'hover:bg-gray-100'}`}
          >
            All Categories
          </button>
          {facets?.categories?.map(c => (
            <button
              key={c.id}
              onClick={() => update('category_id', c.id)}
              className={`flex justify-between w-full text-left text-sm px-2 py-1 rounded ${
                Number(filters.category_id) === c.id ? 'bg-primary text-white' : c.count === 0 ? 'text-gray-300' : 'hover:bg-gray-100'
              }`}
              disabled={c.count === 0}
            >
              <span>{c.name}</span>
              <span className={`text-xs ${Number(filters.category_id) === c.id ? 'text-white/70' : 'text-gray-400'}`}>
                {c.count}
              </span>
            </button>
          ))}
        </div>
      </CollapsibleSection>

      {/* Tire Type */}
      <CollapsibleSection title="Tire Type">
        <div className="space-y-1 max-h-48 overflow-y-auto">
          <button
            onClick={() => update('tire_type', null)}
            className={`block w-full text-left text-sm px-2 py-1 rounded ${!filters.tire_type ? 'bg-primary text-white' : 'hover:bg-gray-100'}`}
          >
            All Types
          </button>
          {facets?.tire_types?.map(t => (
            <button
              key={t.value}
              onClick={() => update('tire_type', t.value)}
              className={`flex justify-between w-full text-left text-sm px-2 py-1 rounded ${
                filters.tire_type === t.value ? 'bg-primary text-white' : t.count === 0 ? 'text-gray-300' : 'hover:bg-gray-100'
              }`}
              disabled={t.count === 0}
            >
              <span>{t.value}</span>
              <span className={`text-xs ${filters.tire_type === t.value ? 'text-white/70' : 'text-gray-400'}`}>
                {t.count}
              </span>
            </button>
          ))}
        </div>
      </CollapsibleSection>

      {/* Tire Size */}
      <CollapsibleSection title="Tire Size" defaultOpen={false}>
        <div className="space-y-1 max-h-48 overflow-y-auto">
          <button
            onClick={() => update('tire_size', null)}
            className={`block w-full text-left text-sm px-2 py-1 rounded ${!filters.tire_size ? 'bg-primary text-white' : 'hover:bg-gray-100'}`}
          >
            All Sizes
          </button>
          {facets?.tire_sizes?.map(s => (
            <button
              key={s.value}
              onClick={() => update('tire_size', s.value)}
              className={`flex justify-between w-full text-left text-sm px-2 py-1 rounded font-mono ${
                filters.tire_size === s.value ? 'bg-primary text-white' : s.count === 0 ? 'text-gray-300' : 'hover:bg-gray-100'
              }`}
              disabled={s.count === 0}
            >
              <span>{s.value}</span>
              <span className={`text-xs font-sans ${filters.tire_size === s.value ? 'text-white/70' : 'text-gray-400'}`}>
                {s.count}
              </span>
            </button>
          ))}
        </div>
      </CollapsibleSection>

      {/* Age / FEFO Status */}
      <CollapsibleSection title="Tire Age (FEFO)">
        <div className="space-y-1">
          <button
            onClick={() => update('age_category', null)}
            className={`block w-full text-left text-sm px-2 py-1 rounded ${!filters.age_category ? 'bg-primary text-white' : 'hover:bg-gray-100'}`}
          >
            All Ages
          </button>
          {facets?.age_categories?.map(a => (
            <button
              key={a.value}
              onClick={() => update('age_category', a.value)}
              className={`flex justify-between items-center w-full text-left text-sm px-2 py-1 rounded ${
                filters.age_category === a.value ? 'bg-primary text-white' : 'hover:bg-gray-100'
              }`}
            >
              {filters.age_category === a.value ? (
                <span className="capitalize">{a.value}</span>
              ) : (
                <AgeBadge ageCategory={a.value} discountPercent={0} />
              )}
              <span className={`text-xs ${filters.age_category === a.value ? 'text-white/70' : 'text-gray-400'}`}>
                {a.count}
              </span>
            </button>
          ))}
        </div>
      </CollapsibleSection>

      {/* Price Range */}
      <CollapsibleSection title="Price Range">
        <div className="space-y-1">
          <button
            onClick={() => { update('min_price', null); onChange(f => ({ ...f, max_price: null, page: 1 })) }}
            className={`block w-full text-left text-sm px-2 py-1 rounded ${
              !filters.min_price && !filters.max_price ? 'bg-primary text-white' : 'hover:bg-gray-100'
            }`}
          >
            Any Price
          </button>
          {facets?.price_ranges?.map(pr => (
            <button
              key={pr.label}
              onClick={() => onChange({
                ...filters,
                min_price: pr.min_val || null,
                max_price: pr.max_val || null,
                page: 1,
              })}
              className={`flex justify-between w-full text-left text-sm px-2 py-1 rounded ${
                pr.count === 0 ? 'text-gray-300' : 'hover:bg-gray-100'
              }`}
              disabled={pr.count === 0}
            >
              <span>{pr.label}</span>
              <span className="text-xs text-gray-400">{pr.count}</span>
            </button>
          ))}
        </div>
      </CollapsibleSection>

      {/* In Stock Toggle */}
      <div className="mb-4">
        <label className="flex items-center gap-2 text-sm cursor-pointer">
          <input
            type="checkbox"
            checked={!!filters.in_stock}
            onChange={e => update('in_stock', e.target.checked || null)}
            className="rounded border-gray-300 text-primary focus:ring-primary"
          />
          In Stock Only
        </label>
      </div>

      <button
        onClick={() => onChange({ page: 1, per_page: 20 })}
        className="w-full text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 py-1.5 rounded transition"
      >
        Reset All Filters
      </button>
    </aside>
  )
}
