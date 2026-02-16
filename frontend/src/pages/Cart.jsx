import { Link } from 'react-router-dom'
import { useCart } from '../context/CartContext'

export default function Cart() {
  const { cart, removeFromCart, updateQuantity, getCartTotal, clearCart } = useCart()

  if (cart.length === 0) {
    return (
      <div className="text-center py-16 bg-white rounded-lg shadow">
        <div className="text-5xl mb-4">&#128722;</div>
        <h2 className="text-xl font-bold text-primary mb-2">Your cart is empty</h2>
        <p className="text-gray-500 mb-6">Browse our catalog to find the tires you need.</p>
        <Link to="/catalog" className="bg-primary hover:bg-primary-light text-white font-bold py-2.5 px-6 rounded-lg transition">
          Browse Catalog
        </Link>
      </div>
    )
  }

  const subtotal = getCartTotal()
  const tax = subtotal * 0.07
  const total = subtotal + tax

  return (
    <div>
      <h1 className="text-2xl font-bold text-primary mb-6">Shopping Cart</h1>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Items */}
        <div className="lg:col-span-2 space-y-3">
          {/* Header */}
          <div className="hidden md:grid grid-cols-12 gap-4 text-xs text-gray-500 uppercase tracking-wide px-4">
            <div className="col-span-5">Product</div>
            <div className="col-span-2 text-right">Price</div>
            <div className="col-span-2 text-center">Qty</div>
            <div className="col-span-2 text-right">Total</div>
            <div className="col-span-1"></div>
          </div>

          {cart.map(item => (
            <div key={item.product_id} className="bg-white rounded-lg shadow p-4">
              <div className="grid grid-cols-12 gap-4 items-center">
                <div className="col-span-12 md:col-span-5">
                  <Link to={`/products/${item.product_id}`} className="font-semibold text-primary hover:underline text-sm">
                    {item.product.name}
                  </Link>
                  <p className="text-xs text-gray-500">{item.product.tire_size} &middot; {item.product.brand_name}</p>
                </div>
                <div className="col-span-4 md:col-span-2 text-right text-sm">
                  ${Number(item.product.wholesale_price).toFixed(2)}
                </div>
                <div className="col-span-4 md:col-span-2 flex items-center justify-center gap-1">
                  <button
                    onClick={() => updateQuantity(item.product_id, item.quantity - 1)}
                    className="w-7 h-7 rounded border text-sm hover:bg-gray-100"
                  >-</button>
                  <span className="w-8 text-center text-sm">{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.product_id, item.quantity + 1)}
                    className="w-7 h-7 rounded border text-sm hover:bg-gray-100"
                  >+</button>
                </div>
                <div className="col-span-2 md:col-span-2 text-right font-semibold text-sm">
                  ${(Number(item.product.wholesale_price) * item.quantity).toFixed(2)}
                </div>
                <div className="col-span-2 md:col-span-1 text-right">
                  <button
                    onClick={() => removeFromCart(item.product_id)}
                    className="text-red-500 hover:text-red-700 text-xs"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))}

          <div className="flex justify-between items-center pt-2">
            <button onClick={clearCart} className="text-sm text-red-500 hover:text-red-700">
              Clear Cart
            </button>
            <Link to="/catalog" className="text-sm text-primary hover:underline">
              Continue Shopping
            </Link>
          </div>
        </div>

        {/* Summary */}
        <div>
          <div className="bg-white rounded-lg shadow p-6 sticky top-24">
            <h2 className="font-bold text-primary mb-4">Order Summary</h2>
            <div className="space-y-2 text-sm mb-4">
              <div className="flex justify-between">
                <span className="text-gray-600">Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Tax (7%)</span>
                <span>${tax.toFixed(2)}</span>
              </div>
            </div>
            <div className="border-t pt-3 mb-6">
              <div className="flex justify-between text-lg font-bold">
                <span>Total</span>
                <span className="text-secondary">${total.toFixed(2)}</span>
              </div>
            </div>
            <Link
              to="/checkout"
              className="block w-full bg-secondary hover:bg-secondary-dark text-white text-center font-bold py-3 rounded-lg transition"
            >
              Place Order
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
