import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [apiStatus, setApiStatus] = useState('checking');
  const [apiData, setApiData] = useState(null);

  useEffect(() => {
    // Check API connection
    fetch('http://localhost:5000/')
      .then(res => res.json())
      .then(data => {
        setApiStatus('connected');
        setApiData(data);
      })
      .catch(err => {
        setApiStatus('disconnected');
        console.error('API connection error:', err);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎓 PhD Application Automator</h1>
        <p className="tagline">AI-Powered Global PhD Opportunity Discovery</p>

        <div className={`status-badge ${apiStatus}`}>
          <span className="status-dot"></span>
          API Status: {apiStatus === 'connected' ? '✅ Connected' : apiStatus === 'checking' ? '🔄 Checking...' : '❌ Disconnected'}
        </div>

        {apiData && (
          <div className="api-info">
            <h2>Backend API Information</h2>
            <div className="info-grid">
              <div className="info-item">
                <strong>Name:</strong> {apiData.name}
              </div>
              <div className="info-item">
                <strong>Version:</strong> {apiData.version}
              </div>
              <div className="info-item">
                <strong>Status:</strong> {apiData.status}
              </div>
            </div>
          </div>
        )}

        <div className="features">
          <h2>✨ Key Features</h2>
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">🌍</div>
              <h3>Global Discovery</h3>
              <p>Discover PhD opportunities in 195+ countries worldwide</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered Matching</h3>
              <p>Intelligent research area matching with Gemini AI</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📧</div>
              <h3>Automated Emails</h3>
              <p>Personalized email generation and batch sending</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Application Tracking</h3>
              <p>Monitor responses and manage your applications</p>
            </div>
          </div>
        </div>

        <div className="getting-started">
          <h2>🚀 Getting Started</h2>
          <div className="steps">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3>Configure Backend</h3>
                <p>Edit <code>backend/.env</code> with your API keys and SMTP settings</p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3>Register Account</h3>
                <p>Create your account via API: <code>POST /api/auth/register</code></p>
              </div>
            </div>
            <div className="step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3>Discover Opportunities</h3>
                <p>Start discovering universities and professors worldwide</p>
              </div>
            </div>
          </div>
        </div>

        <div className="api-endpoints">
          <h2>📚 API Endpoints</h2>
          <div className="endpoint-list">
            <div className="endpoint">
              <span className="method method-get">GET</span>
              <code>/api/health</code>
              <span className="description">Health check</span>
            </div>
            <div className="endpoint">
              <span className="method method-post">POST</span>
              <code>/api/auth/register</code>
              <span className="description">Register new user</span>
            </div>
            <div className="endpoint">
              <span className="method method-post">POST</span>
              <code>/api/auth/login</code>
              <span className="description">User login</span>
            </div>
            <div className="endpoint">
              <span className="method method-get">GET</span>
              <code>/api/universities/search</code>
              <span className="description">Search universities</span>
            </div>
            <div className="endpoint">
              <span className="method method-get">GET</span>
              <code>/api/professors/search</code>
              <span className="description">Search professors</span>
            </div>
            <div className="endpoint">
              <span className="method method-post">POST</span>
              <code>/api/emails/generate</code>
              <span className="description">Generate personalized emails</span>
            </div>
          </div>
          <a href="http://localhost:5000/api/docs" target="_blank" rel="noopener noreferrer" className="view-all-link">
            View All API Endpoints →
          </a>
        </div>

        <div className="footer">
          <p>Made with ❤️ for PhD Applicants Worldwide</p>
          <p className="version">Version 1.0.0 | Open Source</p>
        </div>
      </header>
    </div>
  );
}

export default App;
