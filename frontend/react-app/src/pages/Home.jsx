import React from 'react'

function Hero(){
  return (
    <section className="hero" aria-labelledby="home-hero">
      <div className="hero-copy">
        <h1 id="home-hero">Find colleges, courses and apply easily</h1>
        <p className="lead">Search colleges, compare programs and apply with a single form. Mobile and desktop friendly design.</p>
        <div className="cta-row">
          <a className="btn" href="/colleges/">Explore Colleges</a>
          <a className="btn ghost" href="/apply/">Apply Now</a>
        </div>
      </div>
      <div className="hero-media card" aria-hidden>
        <div style={{width: '100%', height: '180px', background: 'linear-gradient(90deg,#ff6a3d33,#ff8a0033)', borderRadius:8}}></div>
      </div>
    </section>
  )
}

function CollegeList(){
  const items = [
    {id:1, name:'Example Institute of Technology', city:'Mumbai'},
    {id:2, name:'National College of Arts', city:'Delhi'},
    {id:3, name:'City University', city:'Bangalore'},
  ]
  return (
    <section>
      <h2>Popular Colleges</h2>
      <div className="row gap-24 mt-16">
        {items.map(c => (
          <div key={c.id} className="card col">
            <h3 style={{margin:'0 0 8px 0'}}>{c.name}</h3>
            <p className="u-muted">{c.city}</p>
            <div className="mt-8">
              <a className="btn" href={`/college/${c.id}/`}>View</a>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}

export default function Home(){
  return (
    <div>
      <Hero />
      <div className="mt-16">
        <CollegeList />
      </div>
    </div>
  )
}
