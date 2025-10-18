
import React, { useEffect } from 'react';
import './App.css';

export default function App() {
  const dj = window.__DJANGO__ || {};
  useEffect(() => {
    if (dj.page_background_url) document.documentElement.style.setProperty('--page-bg-url', `url('${dj.page_background_url}')`);
  }, [dj.page_background_url]);

  return (
    <div className="app-root">
      <header className="header-yellow">
        <div className="header-title">AdmitionWala</div>
        <nav className="header-nav">
          <a href="#explore">Explore</a>
          <a href="#apply">Apply</a>
          <a href="#courses">Courses</a>
        </nav>
      </header>
      <main className="main-content">
        <h1 className="hero-title">Find. Match. Apply.</h1>
        <p className="hero-desc">
          Guiding students and parents to find the right college. Building a better future, one student at a time.
        </p>
        <div className="button-group-vertical">
          <a href="#explore" className="button-orange">Explore Colleges</a>
          <a href="#apply" className="button-orange">Apply Now</a>
          <a href="#courses" className="button-orange">Our Certified Courses</a>
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
