import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import api from '../api/client'
import { useCart } from '../context/CartContext'
import AgeBadge from '../components/AgeBadge'

export default function Checkout() {
  const navigate = useNavigate()
  const { cart, getCartTotal, clearCart } = useCart()
  const [form, setForm] = useState({ dealer_name: '', dealer_email: '', notes: '' })
  const [errors, setErrors] = useState({})
  const [orderResult, setOrderResult] = useState(null)

  const mutation = useMutation({
    mutationFn: (data) => api.post('/orders', data).then(r => r.data),
    onSuccess: (data) => {
      clearCart()
      setOrderResult(data)
    },
  })

  if (cart.length === 0 && !orderResult) {
    return (
      <div className="text-center py-16 bg-white rounded-lg shadow">
        <h2 className="text-xl font-bold text-primary mb-2">Your cart is empty</h2>
        <Link to="/catalog" className="text-primary hover:underline">Browse Catalog</Link>
      </div>
    )
  }

  // Order confirmation with FEFO details
  if (orderResult) {
    const hasFefoAllocations = orderResult.items.some(i => i.warehouse_source)
    return (
      <div className="max-w-2xl mx-auto py-8">
        <div className="bg-white rounded-lg shadow p-8 text-center mb-6">
          <div className="text-5xl mb-4">&#9989;</div>
          <h2 className="text-2xl font-bold text-primary mb-2">Order Placed!</h2>
          <p className="text-gray-600 mb-2">Your order has been submitted successfully.</p>
          <p className="text-lg font-mono font-bold text-secondary mb-2">{orderResult.order_number}</p>
          {hasFefoAllocations && (
            <span className="inline-block text-xs bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-medium">
              FEFO Optimized
            </span>
          )}
        </div>

        {/* FEFO Allocation Details */}
        {hasFefoAllocations && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h3 className="font-bold text-primary mb-3">Warehouse Allocation (FEFO)</h3>
            <p className="text-xs text-gray-500 mb-3">
              Items are shipped from the oldest available stock first to minimize waste.
            </p>
            <div className="space-y-2">
              {orderResult.items.map(item => (
                <div key={item.id} className="flex flex-col sm:flex-row sm:justify-between text-sm bg-gray-50 rounded p-3">
                  <div className="flex-1">
                    <span className="font-medium">{item.product?.name || `Product #${item.product_id}`}</span>
                    <span className="text-gray-500 ml-2">{item.product?.tire_size}</span>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-xs text-gray-500">from {item.warehouse_source}</span>
                      {item.age_category && (
                        <AgeBadge ageCategory={item.age_category} discountPercent={item.discount_percent} />
                      )}
                    </div>
                  </div>
                  <div className="text-right mt-2 sm:mt-0">
                    <span className="text-gray-600">{item.quantity} x ${Number(item.unit_price).toFixed(2)}</span>
                    <span className="font-semibold ml-3">${Number(item.line_total).toFixed(2)}</span>
                    {item.discount_percent > 0 && (
                      <span className="block text-xs text-green-600">
                        {item.discount_percent}% age discount applied
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
            <div className="border-t mt-3 pt-3 text-sm">
              <div className="flex justify-between"><span>Subtotal</span><span>${Number(orderResult.subtotal).toFixed(2)}</span></div>
              <div className="flex justify-between"><span>Tax (7%)</span><span>${Number(orderResult.tax).toFixed(2)}</span></div>
              <div className="flex justify-between font-bold text-lg mt-1">
                <span>Total</span><span className="text-secondary">${Number(orderResult.total).toFixed(2)}</span>
              </div>
            </div>
          </div>
        )}

        <div className="flex gap-4 justify-center">
          <Link to="/orders" className="bg-primary hover:bg-primary-light text-white font-bold py-2 px-6 rounded-lg transition">
            View Orders
          </Link>
          <Link to="/catalog" className="border border-primary text-primary hover:bg-gray-50 font-bold py-2 px-6 rounded-lg transition">
            Continue Shopping
          </Link>
        </div>
      </div>
    )
  }

  const validate = () => {
    const e = {}
    if (!form.dealer_name.trim()) e.dealer_name = 'Dealer name is required'
    if (!form.dealer_email.trim()) e.dealer_email = 'Email is required'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.dealer_email)) e.dealer_email = 'Invalid email'
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!validate()) return

    mutation.mutate({
      dealer_name: form.dealer_name.trim(),
      dealer_email: form.dealer_email.trim(),
      notes: form.notes.trim() || null,
      items: cart.map(item => ({
        product_id: item.product_id,
        quantity: item.quantity,
      })),
    })
  }

  const subtotal = getCartTotal()
  const tax = subtotal * 0.07
  const total = subtotal + tax

  return (
    <div>
      <h1 className="text-2xl font-bold text-primary mb-6">Checkout</h1>

      {/* FEFO notice */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-2 mb-6 text-sm text-blue-800">
        <strong>FEFO Notice:</strong> Your order will be fulfilled using First Expired, First Out allocation.
        Older stock ships first. Age-based discounts are applied automatically at checkout.
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        <form onSubmit={handleSubmit} className="lg:col-span-2 bg-white rounded-lg shadow p-6">
          <h2 className="font-bold text-primary mb-4">Dealer Information</h2>

          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Dealer Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={form.dealer_name}
                onChange={e => { setForm(f => ({ ...f, dealer_name: e.target.value })); setErrors(er => ({ ...er, dealer_name: '' })) }}
                className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary ${errors.dealer_name ? 'border-red-500' : ''}`}
              />
              {errors.dealer_name && <p className="text-red-500 text-xs mt-1">{errors.dealer_name}</p>}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Dealer Email <span className="text-red-500">*</span>
              </label>
              <input
                type="email"
                value={form.dealer_email}
                onChange={e => { setForm(f => ({ ...f, dealer_email: e.target.value })); setErrors(er => ({ ...er, dealer_email: '' })) }}
                className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary ${errors.dealer_email ? 'border-red-500' : ''}`}
              />
              {errors.dealer_email && <p className="text-red-500 text-xs mt-1">{errors.dealer_email}</p>}
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">Notes (optional)</label>
            <textarea
              value={form.notes}
              onChange={e => setForm(f => ({ ...f, notes: e.target.value }))}
              rows={3}
              placeholder="Special instructions, delivery preferences..."
              className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          {mutation.isError && (
            <div className="bg-red-50 border border-red-200 text-red-700 rounded p-3 mb-4 text-sm">
              {mutation.error?.response?.data?.detail || 'Failed to place order. Please try again.'}
            </div>
          )}

          <button
            type="submit"
            disabled={mutation.isPending}
            className="w-full bg-secondary hover:bg-secondary-dark text-white font-bold py-3 rounded-lg transition disabled:bg-gray-400"
          >
            {mutation.isPending ? 'Placing Order...' : 'Confirm Order'}
          </button>
        </form>

        {/* Summary */}
        <div>
          <div className="bg-white rounded-lg shadow p-6 sticky top-24">
            <h2 className="font-bold text-primary mb-4">Order Summary</h2>
            <div className="space-y-2 mb-4">
              {cart.map(item => (
                <div key={item.product_id} className="flex justify-between text-sm">
                  <span className="text-gray-600 truncate mr-2">{item.product.name} x{item.quantity}</span>
                  <span className="whitespace-nowrap">${(Number(item.product.wholesale_price) * item.quantity).toFixed(2)}</span>
                </div>
              ))}
            </div>
            <div className="border-t pt-3 space-y-1 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Subtotal</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Tax (7%)</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-lg font-bold pt-2 border-t mt-2">
                <span>Total</span>
                <span className="text-secondary">${total.toFixed(2)}</span>
              </div>
              <p className="text-xs text-gray-400 mt-2">
                * Final total may vary with FEFO age discounts applied at order time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
