import { useState, useEffect } from 'react'
import { onToast } from '../context/CartContext'

export default function Toast() {
  const [message, setMessage] = useState('')
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    return onToast((msg) => {
      setMessage(msg)
      setVisible(true)
      setTimeout(() => setVisible(false), 2500)
    })
  }, [])

  if (!visible) return null

  return (
    <div className="fixed bottom-6 right-6 z-50 bg-primary text-white px-6 py-3 rounded-lg shadow-lg animate-fade-in">
      {message}
    </div>
  )
}
