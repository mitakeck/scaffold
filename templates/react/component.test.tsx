import React from 'react';
import { render, screen } from '@testing-library/react';
import {{name}} from '../{{name}}';

/**
 * {{name}} Component Tests
 * 
 * @author {{author}}
 * @created {{date}}
 */

describe('{{name}}', () => {
  test('renders {{name}} component', () => {
    render(<{{name}} />);
    const element = screen.getByText(/{{name}} Component/i);
    expect(element).toBeInTheDocument();
  });

  test('has correct CSS class', () => {
    const { container } = render(<{{name}} />);
    const component = container.querySelector('.{{name}}');
    expect(component).toBeInTheDocument();
  });

  // Add more tests here
});