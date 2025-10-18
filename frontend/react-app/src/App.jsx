
import React, { useEffect } from 'react';

export default function App() {
  const dj = window.__DJANGO__ || {};
  useEffect(() => {
    if (dj.page_background_url) document.documentElement.style.setProperty('--page-bg-url', `url('${dj.page_background_url}')`);
  }, [dj.page_background_url]);

  return (
    <div style={{ fontFamily: 'Segoe UI, Arial, sans-serif', background: '#f8f8f8', minHeight: '100vh' }}>
      <header
        style={{
          background: '#FFD600', // bright yellow
          color: '#222',
          padding: '18px 0',
          boxShadow: '0 2px 12px rgba(0,0,0,0.07)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          position: 'sticky',
          top: 0,
          zIndex: 100,
        }}
      >
        <div style={{ fontWeight: 700, fontSize: '2rem', letterSpacing: '1px', marginBottom: 4 }}>
          AdmitionWala
        </div>
        <nav style={{ display: 'flex', gap: 24, marginTop: 6 }}>
          <a href="#explore" style={navLinkStyle}>Explore</a>
          <a href="#apply" style={navLinkStyle}>Apply</a>
          <a href="#courses" style={navLinkStyle}>Courses</a>
        </nav>
      </header>
      <main style={{ maxWidth: 600, margin: '32px auto', background: '#fff', borderRadius: 12, boxShadow: '0 2px 12px rgba(0,0,0,0.04)', padding: 24 }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, marginBottom: 12, textAlign: 'center' }}>Find. Match. Apply.</h1>
        <p style={{ fontSize: '1.1rem', color: '#444', marginBottom: 24, textAlign: 'center' }}>
          Guiding students and parents to find the right college. Building a better future, one student at a time.
        </p>
        <div style={buttonGroupStyle}>
          <a href="#explore" style={buttonStyle}>Explore Colleges</a>
          <a href="#apply" style={buttonStyle}>Apply Now</a>
          <a href="#courses" style={buttonStyle}>Our Certified Courses</a>
        </div>
        <section style={{ textAlign: 'center', marginTop: 24 }}>
          <h2 style={{ fontSize: '1.3rem', fontWeight: 600, marginBottom: 10 }}>About Us</h2>
          <div style={{ background: '#222', color: '#fff', borderRadius: '50%', width: 120, height: 120, margin: '0 auto 12px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: 22 }}>
            Counsel
          </div>
          <div style={{ fontWeight: 500, color: '#222' }}>ADMITIONWALA</div>
          <div style={{ fontSize: 13, color: '#888', marginTop: 4 }}>Innovating Online Learning</div>
        </section>
      </main>
      <style>{`
        @media (max-width: 700px) {
          .button-group-vertical {
            flex-direction: column !important;
            gap: 14px !important;
            align-items: stretch !important;
          }
        }
      `}</style>
    </div>
  );
}

const navLinkStyle = {
  color: '#222',
  textDecoration: 'none',
  fontWeight: 500,
  fontSize: 16,
  padding: '4px 10px',
  borderRadius: 4,
  transition: 'background 0.2s',
};

const buttonGroupStyle = {
  display: 'flex',
  flexDirection: 'column',
  gap: 18,
  alignItems: 'stretch',
  marginBottom: 32,
  width: '100%',
  maxWidth: 320,
  marginLeft: 'auto',
  marginRight: 'auto',
  className: 'button-group-vertical',
};

const buttonStyle = {
  background: '#FF8000',
  color: '#fff',
  fontWeight: 600,
  fontSize: 17,
  padding: '14px 0',
  width: '100%',
  border: 'none',
  borderRadius: 7,
  textAlign: 'center',
  textDecoration: 'none',
  boxShadow: '0 1px 6px rgba(0,0,0,0.07)',
  transition: 'background 0.2s',
  cursor: 'pointer',
  marginBottom: 0,
};
