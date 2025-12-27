// src/app/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import './styles/globals.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// src/app/App.tsx
import { Providers } from './providers';
import { Router } from './router';

export function App() {
  return (
    <Providers>
      <Router />
    </Providers>
  );
}