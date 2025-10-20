import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import Header from '../src/components/Header'

describe('Header overlay accessibility', () => {
  test('opens overlay when toggle clicked and closes on ESC', async () => {
    render(<Header userAuthenticated={false} />)
    const toggle = screen.getByRole('button', { name: /toggle menu/i })
    // Click to open
    fireEvent.click(toggle)
    const overlay = document.querySelector('.mobile-nav-overlay')
    expect(overlay).toHaveClass('open')
    // Press Escape
    fireEvent.keyDown(document, { key: 'Escape', code: 'Escape' })
    expect(overlay).not.toHaveClass('open')
  })
})
