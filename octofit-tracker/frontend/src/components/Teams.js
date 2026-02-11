import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;
      console.log('Fetching teams from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Teams data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) return (
    <div className="loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading teams...</p>
    </div>
  );
  
  if (error) return (
    <div className="error-container">
      <h4>⚠️ Error Loading Teams</h4>
      <p>{error}</p>
      <button className="btn btn-outline-danger" onClick={() => window.location.reload()}>Retry</button>
    </div>
  );

  return (
    <div className="container mt-4">
      <div className="component-header">
        <h2>👥 Teams</h2>
        <p className="text-muted mb-0">Join a team and compete together</p>
      </div>
      <div className="p-4 bg-white rounded-bottom shadow-sm">
        <div className="row">
          {teams.length > 0 ? (
            teams.map((team) => (
              <div key={team.id} className="col-md-4 mb-4">
                <div className="card h-100">
                  <div className="card-body d-flex flex-column">
                    <h5 className="card-title">👥 {team.name}</h5>
                    <p className="card-text flex-grow-1">{team.description}</p>
                    <div className="mt-auto">
                      <span className="badge bg-primary">
                        {team.member_count || team.members?.length || 0} Members
                      </span>
                    </div>
                  </div>
                  <div className="card-footer bg-transparent border-0">
                    <button className="btn btn-sm btn-outline-primary w-100">View Team</button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-12">
              <p className="no-data">No teams found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Teams;
