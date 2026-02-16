import { Link } from 'react-router-dom'
import { useCart } from '../context/CartContext'
import AgeBadge from './AgeBadge'

function stockBadge(qty) {
  if (qty > 50) return 'bg-green-100 text-green-800'
  if (qty >= 10) return 'bg-yellow-100 text-yellow-800'
  if (qty > 0) return 'bg-red-100 text-red-800'
  return 'bg-gray-100 text-gray-500'
}

export default function ProductCard({ product }) {
  const { addToCart } = useCart()
  const hasDiscount = product.discount_percent > 0
  const effectivePrice = Number(product.effective_price || product.wholesale_price)
  const wholesalePrice = Number(product.wholesale_price)

  return (
    <div className="bg-white rounded-lg shadow hover:shadow-md transition flex flex-col">
      <Link to={`/products/${product.id}`} className="p-4 flex-1">
        <div className="flex justify-between items-start mb-2">
          <span className="text-xs text-gray-500 uppercase tracking-wide">{product.brand_name}</span>
          <span className={`text-xs px-2 py-0.5 rounded-full ${stockBadge(product.stock_quantity)}`}>
            {product.stock_quantity > 0 ? `${product.stock_quantity} in stock` : 'Out of stock'}
          </span>
        </div>
        <h3 className="font-semibold text-primary mb-1 leading-tight">{product.name}</h3>
        <p className="text-sm text-gray-500 mb-1">{product.tire_size}</p>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-xs text-gray-400">{product.tire_type}</span>
          {product.age_category && (
            <AgeBadge
              ageCategory={product.age_category}
              dotCode={product.dot_code}
              discountPercent={product.discount_percent}
            />
          )}
        </div>
        <div className="flex items-baseline gap-2">
          {hasDiscount ? (
            <>
              <span className="text-xl font-bold text-green-600">${effectivePrice.toFixed(2)}</span>
              <span className="text-sm text-gray-400 line-through">${wholesalePrice.toFixed(2)}</span>
            </>
          ) : (
            <>
              <span className="text-xl font-bold text-secondary">${wholesalePrice.toFixed(2)}</span>
              {product.msrp && (
                <span className="text-sm text-gray-400 line-through">${Number(product.msrp).toFixed(2)}</span>
              )}
            </>
          )}
        </div>
      </Link>
      <div className="px-4 pb-4">
        <button
          onClick={() => addToCart(product)}
          disabled={product.stock_quantity === 0}
          className="w-full bg-primary hover:bg-primary-light text-white text-sm font-medium py-2 rounded transition disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
        </button>
      </div>
    </div>
  )
}
