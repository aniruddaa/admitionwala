import React, { useState, useRef, useEffect } from 'react'

function firstFocusable(container){
  if(!container) return null
  const selectors = 'a[href], area[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), button:not([disabled]), [tabindex]:not([tabindex="-1"])'
  return container.querySelector(selectors)
}

export default function Header({ userAuthenticated=false, pageBackground=null }){
  const [open, setOpen] = useState(false)
  const overlayRef = useRef(null)
  const toggleRef = useRef(null)
  const lastFocusedRef = useRef(null)

  useEffect(()=>{
    const overlay = overlayRef.current
    const toggle = toggleRef.current
    const main = document.getElementById('main-content')

    function onKey(e){
      if(e.key === 'Escape'){
        setOpen(false)
        return
      }
      if(e.key === 'Tab' && overlay && overlay.classList.contains('open')){
        const focusable = overlay.querySelectorAll('a,button,input,select,textarea,[tabindex]:not([tabindex="-1"])')
        if(focusable.length === 0){ e.preventDefault(); return }
        const first = focusable[0]
        const last = focusable[focusable.length -1]
        if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
        else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
      }
    }

    if(open){
      lastFocusedRef.current = document.activeElement
      document.body.style.overflow = 'hidden'
      overlay && overlay.classList.add('open')
      if(main) main.setAttribute('aria-hidden','true')
      // focus first focusable in the overlay
      const f = firstFocusable(overlay)
      if(f) f.focus()
      document.addEventListener('keydown', onKey)
    } else {
      document.body.style.overflow = ''
      overlay && overlay.classList.remove('open')
      if(main) main.setAttribute('aria-hidden','false')
      if(lastFocusedRef.current && typeof lastFocusedRef.current.focus === 'function') lastFocusedRef.current.focus()
      document.removeEventListener('keydown', onKey)
    }

    return ()=>{ document.removeEventListener('keydown', onKey); document.body.style.overflow = ''; if(main) main.setAttribute('aria-hidden','false') }
  },[open])

  return (
    <header className="site-header">
      <div className="inner">
  <div className="logo"><a href="/" style={{display:'flex',alignItems:'center',gap:8}}><img src="/static/images/admitionwala_logo.svg" alt="logo"/><span className="brand-word">AdmitionWala</span></a></div>
        <nav className="main-nav" aria-hidden={open ? 'true' : 'false'} style={{display: open ? 'block' : 'flex'}}>
          <a href="/colleges/">Explore</a>
          <a href="/courses/">Courses</a>
          <a href="/careers/">Careers</a>
          <a href="/about/">About</a>
        </nav>
        <div style={{display:'flex',gap:12,alignItems:'center'}}>
          <a className="btn ghost" href="/apply/">Apply</a>
          {userAuthenticated ? (
            <a className="btn" href="/profile/">Account</a>
          ) : (
            <a className="btn outline" href="/login/">Login</a>
          )}
          {/* Prominent CTA as pill */}
          <a className="main-cta btn btn--primary-pill" href="/apply/">Apply Now</a>
          <button ref={toggleRef} className={`menu-toggle ${open ? 'is-open' : ''}`} aria-label="Toggle menu" aria-expanded={open} aria-controls="mobileNav" onClick={()=>setOpen(s=>!s)}>
            <svg viewBox="0 0 24 18" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true">
              <g stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                <path className="bar top" d="M2 3h20"/>
                <path className="bar mid" d="M2 9h20"/>
                <path className="bar bot" d="M2 15h20"/>
              </g>
            </svg>
          </button>
        </div>
      </div>
      <div ref={overlayRef} className={"mobile-nav-overlay" + (open ? ' open' : '')} id="mobileNav" aria-hidden={!open} aria-modal={open} role="dialog">
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center'}}>
          <div><img src="/static/images/admitionwala_logo.svg" alt="small logo" style={{height:36}}/></div>
          <button onClick={()=>setOpen(false)} aria-label="Close menu" style={{fontSize:28,background:'transparent',border:0,color:'#fff'}}>×</button>
        </div>
        <div className="links" style={{marginTop:18}}>
          <a href="/colleges/">Explore Colleges</a>
          <a href="/courses/">All Courses</a>
          <a href="/careers/">Careers</a>
          <a href="/about/">About</a>
          <a className="cta" href="/apply/">Apply Now</a>
        </div>
      </div>
    </header>
  )
}
