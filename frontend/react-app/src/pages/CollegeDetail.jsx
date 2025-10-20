import React from 'react'

export default function CollegeDetail(){
  return (
    <article className="card">
      <h2>College Name</h2>
      <p className="u-muted">City — State</p>
      <div className="mt-16">
        <a className="btn" href="#apply">Apply to this college</a>
      </div>
    </article>
  )
}
