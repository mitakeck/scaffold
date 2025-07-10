import './App.css'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>{{name}}</h1>
        <p>{{description}}</p>
        <p className="app-info">
          Created by {{author}} on {{date}}
        </p>
      </header>
      <main className="app-main">
        <section className="welcome-section">
          <h2>Welcome to your new React TypeScript project!</h2>
          <p>
            This project was generated with Vite, React, TypeScript, ESLint, and Prettier.
          </p>
          
          <div className="quick-start">
            <h3>Quick Start</h3>
            <ol>
              <li>Run <code>npm install</code> to install dependencies</li>
              <li>Run <code>npm run dev</code> to start the development server</li>
              <li>Edit <code>src/App.tsx</code> to customize this page</li>
            </ol>
          </div>

          <div className="available-scripts">
            <h3>Available Scripts</h3>
            <ul>
              <li><code>npm run dev</code> - Start development server</li>
              <li><code>npm run build</code> - Build for production</li>
              <li><code>npm run lint</code> - Run ESLint</li>
              <li><code>npm run format</code> - Format code with Prettier</li>
              <li><code>npm run test</code> - Run tests with Vitest</li>
            </ul>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App