import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './index.css'

// Mount into the existing #react-root created by Django templates
const mountEl = document.getElementById('react-root') || document.getElementById('root') || document.body.appendChild(document.createElement('div'));
if (mountEl) createRoot(mountEl).render(<App />)
