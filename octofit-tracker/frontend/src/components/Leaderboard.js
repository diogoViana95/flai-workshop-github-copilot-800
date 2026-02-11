import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/leaderboard/`;
      console.log('Fetching leaderboard from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Leaderboard data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  if (loading) return (
    <div className="loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading leaderboard...</p>
    </div>
  );
  
  if (error) return (
    <div className="error-container">
      <h4>⚠️ Error Loading Leaderboard</h4>
      <p>{error}</p>
      <button className="btn btn-outline-danger" onClick={() => window.location.reload()}>Retry</button>
    </div>
  );

  const getRankBadge = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  return (
    <div className="container mt-4">
      <div className="component-header">
        <h2>🏆 Leaderboard</h2>
        <p className="text-muted mb-0">Top performers in the OctoFit community</p>
      </div>
      <div className="table-container">
        <div className="table-responsive">
          <table className="table table-hover">
            <thead>
              <tr>
                <th scope="col">Rank</th>
                <th scope="col">User</th>
                <th scope="col">Total Calories</th>
                <th scope="col">Activities</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.length > 0 ? (
                leaderboard.map((entry, index) => (
                  <tr key={entry.user_id || index} className={index < 3 ? 'table-light' : ''}>
                    <td><h5 className="mb-0">{getRankBadge(index + 1)}</h5></td>
                    <td><strong>{entry.user_name || entry.username}</strong></td>
                    <td><span className="badge bg-danger">{entry.total_calories || 0} cal</span></td>
                    <td><span className="badge bg-primary">{entry.total_activities || 0}</span></td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="no-data">No leaderboard data found</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
