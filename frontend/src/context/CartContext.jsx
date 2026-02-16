import { createContext, useContext, useState, useEffect, useCallback } from 'react'

const CartContext = createContext()

export function useCart() {
  const ctx = useContext(CartContext)
  if (!ctx) throw new Error('useCart must be used within CartProvider')
  return ctx
}

// Simple event emitter for toast notifications
const toastListeners = []
export function onToast(fn) {
  toastListeners.push(fn)
  return () => {
    const i = toastListeners.indexOf(fn)
    if (i >= 0) toastListeners.splice(i, 1)
  }
}
function emitToast(message) {
  toastListeners.forEach(fn => fn(message))
}

export function CartProvider({ children }) {
  const [cart, setCart] = useState(() => {
    try {
      const saved = localStorage.getItem('tirepro_cart')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })

  useEffect(() => {
    localStorage.setItem('tirepro_cart', JSON.stringify(cart))
  }, [cart])

  const addToCart = useCallback((product, quantity = 1) => {
    setCart(prev => {
      const existing = prev.find(item => item.product_id === product.id)
      if (existing) {
        emitToast(`Updated ${product.name} quantity in cart`)
        return prev.map(item =>
          item.product_id === product.id
            ? { ...item, quantity: item.quantity + quantity }
            : item
        )
      }
      emitToast(`Added ${product.name} to cart`)
      return [...prev, { product_id: product.id, product, quantity }]
    })
  }, [])

  const removeFromCart = useCallback((productId) => {
    setCart(prev => {
      const item = prev.find(i => i.product_id === productId)
      if (item) emitToast(`Removed ${item.product.name} from cart`)
      return prev.filter(i => i.product_id !== productId)
    })
  }, [])

  const updateQuantity = useCallback((productId, quantity) => {
    if (quantity <= 0) {
      removeFromCart(productId)
      return
    }
    setCart(prev =>
      prev.map(item =>
        item.product_id === productId ? { ...item, quantity } : item
      )
    )
  }, [removeFromCart])

  const clearCart = useCallback(() => {
    setCart([])
  }, [])

  const getCartTotal = useCallback(() => {
    return cart.reduce((sum, item) => sum + Number(item.product.wholesale_price) * item.quantity, 0)
  }, [cart])

  const getCartCount = useCallback(() => {
    return cart.reduce((sum, item) => sum + item.quantity, 0)
  }, [cart])

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, updateQuantity, clearCart, getCartTotal, getCartCount }}>
      {children}
    </CartContext.Provider>
  )
}
