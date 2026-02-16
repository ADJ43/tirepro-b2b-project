import { useState, useEffect } from 'react'

export default function SearchBar({ value, onChange }) {
  const [input, setInput] = useState(value || '')

  useEffect(() => {
    setInput(value || '')
  }, [value])

  useEffect(() => {
    const timer = setTimeout(() => {
      if (input !== value) onChange(input)
    }, 300)
    return () => clearTimeout(timer)
  }, [input])

  return (
    <input
      type="text"
      value={input}
      onChange={e => setInput(e.target.value)}
      placeholder="Search tires by name, size, or description..."
      className="w-full border border-gray-300 rounded-lg px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
    />
  )
}
