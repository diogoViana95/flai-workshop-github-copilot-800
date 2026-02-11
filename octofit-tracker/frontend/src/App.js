import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

// Import components
import Users from './components/Users';
import Activities from './components/Activities';
import Teams from './components/Teams';
import Leaderboard from './components/Leaderboard';
import Workouts from './components/Workouts';

function App() {
  console.log('OctoFit Tracker App initialized');
  console.log('Backend API URL:', `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/`);

  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-custom">
          <div className="container-fluid px-4">
            <Link className="navbar-brand d-flex align-items-center" to="/">
              <img 
                src="/octofit-logo-small.svg" 
                alt="OctoFit Logo" 
                className="brand-logo me-2"
              />
              <span className="brand-text">OctoFit Tracker</span>
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav"
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">
                    <span className="nav-icon">👤</span> Users
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">
                    <span className="nav-icon">🏃</span> Activities
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">
                    <span className="nav-icon">👥</span> Teams
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">
                    <span className="nav-icon">🏆</span> Leaderboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">
                    <span className="nav-icon">💪</span> Workouts
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="container-fluid">
          <Routes>
            <Route path="/" element={
              <div className="welcome-section">
                <h1>🏋️ Welcome to OctoFit Tracker</h1>
                <p className="lead">Track your fitness journey with your team!</p>
                <p className="text-muted">Select a section from the navigation menu to get started.</p>
                <div className="mt-4">
                  <Link to="/activities" className="btn btn-primary btn-lg me-2 mb-2">View Activities</Link>
                  <Link to="/leaderboard" className="btn btn-outline-primary btn-lg mb-2">Check Leaderboard</Link>
                </div>
              </div>
            } />
            <Route path="/users" element={<Users />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/teams" element={<Teams />} />
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/workouts" element={<Workouts />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
