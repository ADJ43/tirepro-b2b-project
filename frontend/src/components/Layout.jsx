import Navbar from './Navbar'
import Toast from './Toast'

export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Navbar />
      <main className="flex-1 container mx-auto px-4 py-8 max-w-7xl">
        {children}
      </main>
      <footer className="bg-primary text-white py-6">
        <div className="container mx-auto px-4 text-center text-sm">
          <p>TirePro B2B &mdash; Wholesale Tire Ordering Platform</p>
          <p className="text-gray-300 mt-1">Built by Andres Jose &mdash; Senior Full Stack Developer</p>
        </div>
      </footer>
      <Toast />
    </div>
  )
}
