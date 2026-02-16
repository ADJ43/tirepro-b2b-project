import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
import SearchBar from '../components/SearchBar'
import FilterSidebar from '../components/FilterSidebar'
import ProductCard from '../components/ProductCard'
import Pagination from '../components/Pagination'
import { AgeLegend } from '../components/AgeBadge'

export default function Catalog() {
  const [filters, setFilters] = useState({ page: 1, per_page: 20 })
  const [search, setSearch] = useState('')
  const [sortBy, setSortBy] = useState('')

  const params = { ...filters }
  if (search) params.search = search
  if (sortBy) {
    const [field, order] = sortBy.split(':')
    params.sort_by = field
    params.sort_order = order
  }
  // Remove null/empty values
  Object.keys(params).forEach(k => {
    if (params[k] === null || params[k] === '') delete params[k]
  })

  const { data, isLoading, isError } = useQuery({
    queryKey: ['products', params],
    queryFn: () => api.get('/products', { params }).then(r => r.data),
    keepPreviousData: true,
  })

  return (
    <div>
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
        <h1 className="text-2xl font-bold text-primary">Tire Catalog</h1>
        <AgeLegend />
      </div>

      {/* FEFO info banner */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-2 mb-6 text-sm text-blue-800">
        <strong>FEFO Inventory:</strong> Tires are shipped oldest-first to minimize waste.
        Aging stock (4+ years) is automatically discounted. Filter by age to see availability.
      </div>

      {/* Top bar: search + sort */}
      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <div className="flex-1">
          <SearchBar value={search} onChange={setSearch} />
        </div>
        <select
          value={sortBy}
          onChange={e => setSortBy(e.target.value)}
          className="border rounded-lg px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">Sort by</option>
          <option value="price:asc">Price: Low to High</option>
          <option value="price:desc">Price: High to Low</option>
          <option value="name:asc">Name: A-Z</option>
          <option value="name:desc">Name: Z-A</option>
          <option value="age:asc">Age: Oldest First</option>
          <option value="age:desc">Age: Newest First</option>
        </select>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        <FilterSidebar filters={filters} onChange={setFilters} search={search} />

        <div className="flex-1">
          {isLoading ? (
            <div className="text-center py-16">
              <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-primary border-r-transparent"></div>
              <p className="mt-3 text-gray-500">Loading products...</p>
            </div>
          ) : isError ? (
            <div className="text-center py-16 text-red-600">
              Failed to load products. Please try again.
            </div>
          ) : data?.items?.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-lg shadow">
              <p className="text-gray-500">No products found. Try adjusting your filters.</p>
            </div>
          ) : (
            <>
              <p className="text-sm text-gray-500 mb-4">
                Showing {data.items.length} of {data.total} products
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                {data.items.map(product => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
              <Pagination
                page={data.page}
                totalPages={data.total_pages}
                onChange={p => setFilters(f => ({ ...f, page: p }))}
              />
            </>
          )}
        </div>
      </div>
    </div>
  )
}
