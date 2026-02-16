import { Link, NavLink } from 'react-router-dom'
import { useCart } from '../context/CartContext'

export default function Navbar() {
  const { getCartCount } = useCart()
  const count = getCartCount()

  const linkClass = ({ isActive }) =>
    `hover:text-secondary transition ${isActive ? 'text-secondary font-semibold' : ''}`

  return (
    <nav className="bg-primary text-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4 max-w-7xl">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold tracking-tight">
            <span className="text-secondary">Tire</span>Pro B2B
          </Link>

          <div className="flex gap-6 items-center text-sm">
            <NavLink to="/" className={linkClass} end>Home</NavLink>
            <NavLink to="/catalog" className={linkClass}>Catalog</NavLink>
            <NavLink to="/orders" className={linkClass}>Orders</NavLink>
            <NavLink to="/cart" className={linkClass}>
              <span className="relative">
                Cart
                {count > 0 && (
                  <span className="absolute -top-2 -right-5 bg-secondary text-white rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold">
                    {count}
                  </span>
                )}
              </span>
            </NavLink>
          </div>
        </div>
      </div>
    </nav>
  )
}
