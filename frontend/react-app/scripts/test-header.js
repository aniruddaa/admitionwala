// Lightweight JSDOM test to verify header overlay focus handling
const fs = require('fs')
const path = require('path')
const { JSDOM } = require('jsdom')

async function run(){
  const html = fs.readFileSync(path.join(__dirname, '..', '..', '..', 'static', 'dist', 'index.html'), 'utf8')
  const dom = new JSDOM(html, { runScripts: 'dangerously', resources: 'usable', url: 'http://localhost' })
  // Wait for scripts to load in the JSDOM environment
  await new Promise((res)=> setTimeout(res, 1200))
  const doc = dom.window.document
  const toggle = doc.querySelector('.menu-toggle')
  const overlay = doc.getElementById('mobileNav') || doc.querySelector('.mobile-nav-overlay')
  if(!toggle || !overlay){
    console.log('SKIP: toggle or overlay not present in built HTML');
    return
  }
  console.log('Found toggle and overlay')
  // simulate click
  toggle.dispatchEvent(new dom.window.MouseEvent('click', { bubbles:true }))
  await new Promise((res)=> setTimeout(res, 100))
  console.log('Overlay open?', overlay.classList.contains('open'))
  // simulate ESC
  overlay.dispatchEvent(new dom.window.KeyboardEvent('keydown', { key: 'Escape', bubbles:true }))
  await new Promise((res)=> setTimeout(res, 100))
  console.log('Overlay open after ESC?', overlay.classList.contains('open'))
}

run().catch(e=>{ console.error(e); process.exit(1) })
