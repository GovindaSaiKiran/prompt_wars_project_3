// purpose: Verify basic render | enforces: Test-first
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import React from 'react';

const App = () => <h1>Sustainability Super-App</h1>;

describe('App', () => {
  it('renders headline', () => {
    const { container } = render(<App />);
    expect(container.textContent).toMatch(/Sustainability Super-App/i);
  });
});
