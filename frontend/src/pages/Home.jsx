import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import api from '../api/client'

export default function Home() {
  const { data: brands } = useQuery({
    queryKey: ['brands'],
    queryFn: () => api.get('/brands').then(r => r.data),
  })
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => api.get('/categories').then(r => r.data),
  })
  const { data: products } = useQuery({
    queryKey: ['products-count'],
    queryFn: () => api.get('/products?per_page=1').then(r => r.data),
  })

  const totalProducts = products?.total ?? 0
  const totalBrands = brands?.length ?? 0
  const totalCategories = categories?.length ?? 0

  return (
    <div>
      {/* Hero */}
      <div className="bg-primary text-white rounded-xl py-16 px-8 mb-10 text-center">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="text-secondary">Tire</span>Pro B2B
        </h1>
        <p className="text-xl text-gray-200 mb-8 max-w-2xl mx-auto">
          Your Wholesale Tire Partner &mdash; Premium brands, competitive pricing, and reliable inventory for tire dealers nationwide.
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Link
            to="/catalog"
            className="bg-secondary hover:bg-secondary-dark text-white font-bold py-3 px-8 rounded-lg transition text-lg"
          >
            Browse Catalog
          </Link>
          <Link
            to="/catalog?search="
            className="border-2 border-white hover:bg-white hover:text-primary text-white font-bold py-3 px-8 rounded-lg transition text-lg"
          >
            Search Tires
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <p className="text-4xl font-bold text-secondary">{totalProducts}</p>
          <p className="text-gray-600 mt-1">Products in Stock</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <p className="text-4xl font-bold text-secondary">{totalBrands}</p>
          <p className="text-gray-600 mt-1">Trusted Brands</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <p className="text-4xl font-bold text-secondary">{totalCategories}</p>
          <p className="text-gray-600 mt-1">Tire Categories</p>
        </div>
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-6 mb-12">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold text-primary mb-2">Wide Selection</h3>
          <p className="text-gray-600 text-sm">
            Access to brands like Sumitomo, Multi-Mile, Power King, and more across passenger, truck, commercial, and specialty categories.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold text-primary mb-2">Wholesale Pricing</h3>
          <p className="text-gray-600 text-sm">
            Competitive dealer pricing designed for tire shops and automotive businesses. Volume discounts available.
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-bold text-primary mb-2">Fast Fulfillment</h3>
          <p className="text-gray-600 text-sm">
            Four warehouse locations across the US ensure quick turnaround and reliable shipping to keep your business moving.
          </p>
        </div>
      </div>

      {/* CTA */}
      <div className="bg-gray-100 rounded-xl py-10 px-8 text-center">
        <h2 className="text-2xl font-bold text-primary mb-3">Ready to Order?</h2>
        <p className="text-gray-600 mb-6">Browse our catalog and place your wholesale order today.</p>
        <Link
          to="/catalog"
          className="bg-primary hover:bg-primary-light text-white font-bold py-3 px-8 rounded-lg transition"
        >
          View Products
        </Link>
      </div>
    </div>
  )
}
