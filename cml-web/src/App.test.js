import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

test('renders ABC', () => {
  const { getByText } = render(<App />);
  const linkElement = getByText(/ABC/i);
  expect(linkElement).toBeInTheDocument();
});
