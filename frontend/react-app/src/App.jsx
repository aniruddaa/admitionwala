import React, {useEffect} from 'react'

export default function App(){
  const dj = window.__DJANGO__ || {}
  useEffect(()=>{
    if(dj.page_background_url) document.documentElement.style.setProperty('--page-bg-url', `url('${dj.page_background_url}')`)
  }, [dj.page_background_url])
  return (
    <div>
      <header style={{padding:16}}>AdmitionWala React App (Replace with actual header)</header>
    </div>
  )
}
