import React from 'react'
import Header from './components/Header'
import Footer from './components/Footer'
import Home from './pages/Home'

const DJANGO = typeof window !== 'undefined' && window.__DJANGO__ ? window.__DJANGO__ : { user_authenticated: false, page_background_url: null, static_college_logo: '/static/college_logo.svg' }

export default function App(){
  // If the server rendered a .site-header or main content, avoid duplicating it.
  const hasServerHeader = typeof document !== 'undefined' && !!document.querySelector('.site-header')
  const mainEl = typeof document !== 'undefined' && document.getElementById('main-content')
  const hasServerMain = mainEl && mainEl.innerHTML && mainEl.innerHTML.trim().length > 0

  return (
    <div>
      {/* Only render Header if the template didn't provide one. */}
      {!hasServerHeader && <Header userAuthenticated={DJANGO.user_authenticated} pageBackground={DJANGO.page_background_url} />}

      {/* If server already rendered main content (e.g., /exams/), don't render the React Home page to avoid overwriting admin-provided features. */}
      {!hasServerMain && (
        <>
          <div style={{paddingTop: '12px'}} />
          <main className="container">
            <Home />
          </main>
        </>
      )}

      {/* Footer: if server included a footer element leave it alone; otherwise render React footer. */}
      {!document.querySelector('footer') && <Footer />}
    </div>
  )
}
