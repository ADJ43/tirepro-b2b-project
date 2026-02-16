import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import api from '../api/client'
import { useCart } from '../context/CartContext'
import AgeBadge from '../components/AgeBadge'

function stockBadge(qty) {
  if (qty > 50) return 'bg-green-100 text-green-800'
  if (qty >= 10) return 'bg-yellow-100 text-yellow-800'
  if (qty > 0) return 'bg-red-100 text-red-800'
  return 'bg-gray-100 text-gray-500'
}

export default function ProductDetail() {
  const { id } = useParams()
  const { addToCart } = useCart()
  const [quantity, setQuantity] = useState(1)

  const { data: product, isLoading, isError } = useQuery({
    queryKey: ['product', id],
    queryFn: () => api.get(`/products/${id}`).then(r => r.data),
  })

  // Fetch warehouse inventory (FEFO breakdown)
  const { data: inventory } = useQuery({
    queryKey: ['inventory', id],
    queryFn: () => api.get(`/products/inventory/${id}`).then(r => r.data),
    enabled: !!product,
  })

  if (isLoading) {
    return (
      <div className="text-center py-16">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-primary border-r-transparent"></div>
        <p className="mt-3 text-gray-500">Loading product...</p>
      </div>
    )
  }

  if (isError || !product) {
    return (
      <div className="text-center py-16">
        <p className="text-red-600 mb-4">Product not found.</p>
        <Link to="/catalog" className="text-primary hover:underline">Back to Catalog</Link>
      </div>
    )
  }

  const handleAdd = () => {
    addToCart(product, quantity)
    setQuantity(1)
  }

  const hasDiscount = product.discount_percent > 0
  const effectivePrice = Number(product.effective_price || product.wholesale_price)
  const wholesalePrice = Number(product.wholesale_price)

  return (
    <div>
      <Link to="/catalog" className="text-primary hover:underline text-sm mb-6 inline-block">
        &larr; Back to Catalog
      </Link>

      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="grid md:grid-cols-2 gap-8 p-8">
          {/* Left: image placeholder */}
          <div className="bg-gray-100 rounded-lg flex items-center justify-center min-h-[300px]">
            <div className="text-center text-gray-400">
              <div className="text-6xl mb-2">&#128734;</div>
              <p className="text-sm">{product.tire_size}</p>
            </div>
          </div>

          {/* Right: info */}
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-sm text-gray-500 uppercase tracking-wide">{product.brand_name}</span>
              {product.age_category && (
                <AgeBadge
                  ageCategory={product.age_category}
                  dotCode={product.dot_code}
                  discountPercent={product.discount_percent}
                />
              )}
            </div>
            <h1 className="text-2xl font-bold text-primary mt-1 mb-1">{product.name}</h1>
            <p className="text-lg text-gray-600 mb-4">{product.tire_size}</p>

            <div className="flex items-baseline gap-3 mb-2">
              {hasDiscount ? (
                <>
                  <span className="text-3xl font-bold text-green-600">
                    ${effectivePrice.toFixed(2)}
                  </span>
                  <span className="text-lg text-gray-400 line-through">
                    ${wholesalePrice.toFixed(2)}
                  </span>
                  <span className="text-sm bg-green-100 text-green-800 px-2 py-0.5 rounded-full font-medium">
                    {product.discount_percent}% FEFO Discount
                  </span>
                </>
              ) : (
                <>
                  <span className="text-3xl font-bold text-secondary">
                    ${wholesalePrice.toFixed(2)}
                  </span>
                  {product.msrp && (
                    <span className="text-lg text-gray-400 line-through">
                      MSRP ${Number(product.msrp).toFixed(2)}
                    </span>
                  )}
                </>
              )}
            </div>

            {product.dot_code && (
              <p className="text-xs text-gray-500 mb-4">
                DOT: {product.dot_code} — Manufactured week {product.dot_code.slice(0,2)}, 20{product.dot_code.slice(2,4)}
              </p>
            )}

            <div className="mb-6">
              <span className={`inline-block text-sm px-3 py-1 rounded-full ${stockBadge(product.stock_quantity)}`}>
                {product.stock_quantity > 0 ? `${product.stock_quantity} in stock` : 'Out of stock'}
              </span>
            </div>

            {/* Specs table */}
            <div className="border rounded-lg overflow-hidden mb-6">
              <table className="w-full text-sm">
                <tbody>
                  <tr className="border-b">
                    <td className="px-4 py-2 bg-gray-50 font-medium text-gray-600 w-1/3">Load Index</td>
                    <td className="px-4 py-2">{product.load_index || '---'}</td>
                  </tr>
                  <tr className="border-b">
                    <td className="px-4 py-2 bg-gray-50 font-medium text-gray-600">Speed Rating</td>
                    <td className="px-4 py-2">{product.speed_rating || '---'}</td>
                  </tr>
                  <tr className="border-b">
                    <td className="px-4 py-2 bg-gray-50 font-medium text-gray-600">Type</td>
                    <td className="px-4 py-2">{product.tire_type || '---'}</td>
                  </tr>
                  <tr className="border-b">
                    <td className="px-4 py-2 bg-gray-50 font-medium text-gray-600">Warehouse</td>
                    <td className="px-4 py-2">{product.warehouse_location || '---'}</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-2 bg-gray-50 font-medium text-gray-600">SKU</td>
                    <td className="px-4 py-2 font-mono text-xs">{product.sku}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            {product.description && (
              <p className="text-gray-600 text-sm mb-6">{product.description}</p>
            )}

            {/* Add to cart */}
            <div className="flex gap-3 items-end">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Qty</label>
                <input
                  type="number"
                  min={1}
                  max={product.stock_quantity}
                  value={quantity}
                  onChange={e => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                  className="w-20 border rounded px-3 py-2 text-center focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
              <button
                onClick={handleAdd}
                disabled={product.stock_quantity === 0}
                className="flex-1 bg-secondary hover:bg-secondary-dark text-white font-bold py-2.5 rounded-lg transition disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
              </button>
            </div>
          </div>
        </div>

        {/* Warehouse Inventory (FEFO) */}
        {inventory && inventory.length > 1 && (
          <div className="border-t px-8 py-6">
            <h2 className="font-bold text-primary mb-3 flex items-center gap-2">
              Inventory by Warehouse
              <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full font-normal">
                FEFO — Ships Oldest First
              </span>
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left px-4 py-2 font-medium text-gray-600">Warehouse</th>
                    <th className="text-center px-4 py-2 font-medium text-gray-600">Stock</th>
                    <th className="text-center px-4 py-2 font-medium text-gray-600">DOT Code</th>
                    <th className="text-center px-4 py-2 font-medium text-gray-600">Age</th>
                    <th className="text-right px-4 py-2 font-medium text-gray-600">Price</th>
                    <th className="text-center px-4 py-2 font-medium text-gray-600">Ships</th>
                  </tr>
                </thead>
                <tbody>
                  {inventory.map((inv, i) => (
                    <tr key={inv.product_id} className={`border-t ${inv.ships_first ? 'bg-green-50' : ''}`}>
                      <td className="px-4 py-2">{inv.warehouse}</td>
                      <td className="px-4 py-2 text-center">{inv.stock_quantity}</td>
                      <td className="px-4 py-2 text-center font-mono">{inv.dot_code || '---'}</td>
                      <td className="px-4 py-2 text-center">
                        <AgeBadge
                          ageCategory={inv.age_category}
                          dotCode={inv.dot_code}
                          discountPercent={inv.discount_percent}
                        />
                      </td>
                      <td className="px-4 py-2 text-right">
                        {inv.discount_percent > 0 ? (
                          <span className="text-green-600 font-semibold">${Number(inv.effective_price).toFixed(2)}</span>
                        ) : (
                          <span>${Number(inv.effective_price).toFixed(2)}</span>
                        )}
                      </td>
                      <td className="px-4 py-2 text-center">
                        {inv.ships_first && (
                          <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full font-medium">
                            First
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
