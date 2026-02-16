import { useState, Fragment } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import api from '../api/client'
import AgeBadge from '../components/AgeBadge'

const statusColors = {
  pending: 'bg-yellow-100 text-yellow-800',
  confirmed: 'bg-blue-100 text-blue-800',
  shipped: 'bg-purple-100 text-purple-800',
  delivered: 'bg-green-100 text-green-800',
}

export default function Orders() {
  const [expanded, setExpanded] = useState(null)

  const { data, isLoading, isError } = useQuery({
    queryKey: ['orders'],
    queryFn: () => api.get('/orders').then(r => r.data),
  })

  if (isLoading) {
    return (
      <div className="text-center py-16">
        <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-primary border-r-transparent"></div>
        <p className="mt-3 text-gray-500">Loading orders...</p>
      </div>
    )
  }

  if (isError) {
    return <div className="text-center py-16 text-red-600">Failed to load orders.</div>
  }

  if (!data?.items?.length) {
    return (
      <div className="text-center py-16 bg-white rounded-lg shadow">
        <h2 className="text-xl font-bold text-primary mb-2">No orders yet</h2>
        <p className="text-gray-500 mb-6">Place your first order from our catalog.</p>
        <Link to="/catalog" className="bg-primary hover:bg-primary-light text-white font-bold py-2.5 px-6 rounded-lg transition">
          Browse Catalog
        </Link>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-primary mb-6">Order History</h1>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left px-4 py-3 font-medium text-gray-600">Order #</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600 hidden md:table-cell">Date</th>
              <th className="text-left px-4 py-3 font-medium text-gray-600 hidden md:table-cell">Dealer</th>
              <th className="text-center px-4 py-3 font-medium text-gray-600">Items</th>
              <th className="text-center px-4 py-3 font-medium text-gray-600">Status</th>
              <th className="text-right px-4 py-3 font-medium text-gray-600">Total</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map(order => (
              <Fragment key={order.id}>
                <tr
                  onClick={() => setExpanded(expanded === order.id ? null : order.id)}
                  className="border-t hover:bg-gray-50 cursor-pointer"
                >
                  <td className="px-4 py-3 font-mono text-primary font-semibold">{order.order_number}</td>
                  <td className="px-4 py-3 text-gray-600 hidden md:table-cell">
                    {new Date(order.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3 hidden md:table-cell">{order.dealer_name}</td>
                  <td className="px-4 py-3 text-center">{order.items.length}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${statusColors[order.status] || 'bg-gray-100 text-gray-600'}`}>
                      {order.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right font-semibold">${Number(order.total).toFixed(2)}</td>
                </tr>

                {expanded === order.id && (
                  <tr key={`${order.id}-detail`}>
                    <td colSpan={6} className="bg-gray-50 px-6 py-4">
                      <div className="grid md:grid-cols-2 gap-4 mb-4">
                        <div>
                          <p className="text-xs text-gray-500 uppercase mb-1">Dealer</p>
                          <p className="font-semibold">{order.dealer_name}</p>
                          <p className="text-sm text-gray-600">{order.dealer_email}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-500 uppercase mb-1">Summary</p>
                          <p className="text-sm">Subtotal: ${Number(order.subtotal).toFixed(2)}</p>
                          <p className="text-sm">Tax: ${Number(order.tax).toFixed(2)}</p>
                          <p className="font-semibold">Total: ${Number(order.total).toFixed(2)}</p>
                        </div>
                      </div>
                      {order.notes && (
                        <p className="text-sm text-gray-600 mb-3"><span className="font-medium">Notes:</span> {order.notes}</p>
                      )}
                      <div className="space-y-2">
                        {order.items.map(item => (
                          <div key={item.id} className="flex flex-col sm:flex-row sm:justify-between text-sm bg-white rounded p-3 shadow-sm">
                            <div>
                              <span className="font-medium">{item.product?.name || `Product #${item.product_id}`}</span>
                              <span className="text-gray-500 ml-2">{item.product?.tire_size}</span>
                              <div className="flex items-center gap-2 mt-1">
                                {item.warehouse_source && (
                                  <span className="text-xs text-gray-500">
                                    📦 {item.warehouse_source}
                                  </span>
                                )}
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
                                  {item.discount_percent}% age discount
                                </span>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </td>
                  </tr>
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
