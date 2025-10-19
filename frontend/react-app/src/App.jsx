
import React, { useEffect } from 'react';
import './App.css';

export default function App() {
  const dj = window.__DJANGO__ || {};
  useEffect(() => {
    if (dj.page_background_url) document.documentElement.style.setProperty('--page-bg-url', `url('${dj.page_background_url}')`);
  }, [dj.page_background_url]);

  return (
    <div className="app-root">
      <header className="site-header">
        <div className="logo">
          <img src="/static/images/admitionwala_logo.svg" alt="AdmitionWala" />
        </div>
        <button className="menu-toggle" aria-label="Open menu" aria-expanded="false">
          <svg viewBox="0 0 24 18" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <g stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <path className="bar-top" d="M2 3h20" />
              <path className="bar-mid" d="M2 9h20" />
              <path className="bar-bot" d="M2 15h20" />
            </g>
          </svg>
        </button>
      </header>
      <main className="main-content">
        <h1 className="hero-title">Find. Match. Apply.</h1>
        <p className="hero-desc">
          Guiding students and parents to find the right college. Building a better future, one student at a time.
        </p>
        <div className="cta-row">
          <a href="#explore" className="accent-btn">Explore Colleges</a>
          <a href="#apply" className="accent-btn">Apply Now</a>
          <a href="#courses" className="accent-btn">Our Certified Courses</a>
        </div>
        <section className="about-section">
          <h2 className="about-title">About Us</h2>
          <div className="about-avatar">Counsel</div>
          <div className="about-brand">ADMITIONWALA</div>
          <div className="about-desc">Innovating Online Learning</div>
        </section>
      </main>
    </div>
  );
}
