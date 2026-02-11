import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('cards'); // 'cards' or 'table'
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;
      console.log('Fetching users from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Users data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const usersData = data.results || data;
        setUsers(Array.isArray(usersData) ? usersData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching users:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  // Filter users based on search term
  const filteredUsers = users.filter(user => 
    user.username?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.team_name?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Generate avatar with initials
  const getAvatar = (username) => {
    const initial = username ? username.charAt(0).toUpperCase() : '?';
    const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a'];
    const colorIndex = username ? username.charCodeAt(0) % colors.length : 0;
    return { initial, color: colors[colorIndex] };
  };

  if (loading) return (
    <div className="loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading users...</p>
    </div>
  );
  
  if (error) return (
    <div className="error-container">
      <h4>⚠️ Error Loading Users</h4>
      <p>{error}</p>
      <button className="btn btn-outline-danger" onClick={() => window.location.reload()}>Retry</button>
    </div>
  );

  return (
    <div className="container mt-4">
      <div className="component-header">
        <div className="d-flex justify-content-between align-items-center flex-wrap">
          <div>
            <h2>👤 Users Directory</h2>
            <p className="text-muted mb-0">{filteredUsers.length} registered OctoFit users</p>
          </div>
          <div className="d-flex gap-2 mt-2 mt-md-0">
            <button 
              className={`btn btn-sm ${viewMode === 'cards' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => setViewMode('cards')}
            >
              <span>📇</span> Cards
            </button>
            <button 
              className={`btn btn-sm ${viewMode === 'table' ? 'btn-primary' : 'btn-outline-primary'}`}
              onClick={() => setViewMode('table')}
            >
              <span>📊</span> Table
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white p-3 shadow-sm">
        <div className="search-container mb-4">
          <input
            type="text"
            className="form-control form-control-lg"
            placeholder="🔍 Search by username, email, or team..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {viewMode === 'cards' ? (
          <div className="row g-4">
            {filteredUsers.length > 0 ? (
              filteredUsers.map((user) => {
                const avatar = getAvatar(user.username);
                return (
                  <div key={user.id} className="col-md-6 col-lg-4">
                    <div className="card user-card h-100">
                      <div className="card-body">
                        <div className="d-flex align-items-start mb-3">
                          <div 
                            className="user-avatar me-3"
                            style={{ backgroundColor: avatar.color }}
                          >
                            {avatar.initial}
                          </div>
                          <div className="flex-grow-1">
                            <h5 className="card-title mb-1">{user.username}</h5>
                            <span className="badge bg-secondary user-id-badge">ID: {user.id}</span>
                          </div>
                        </div>
                        
                        <div className="user-details">
                          <div className="detail-item">
                            <span className="detail-icon">📧</span>
                            <a href={`mailto:${user.email}`} className="detail-text">
                              {user.email}
                            </a>
                          </div>
                          
                          <div className="detail-item">
                            <span className="detail-icon">👥</span>
                            {user.team_name || user.team ? (
                              <span className="badge bg-primary">{user.team_name || user.team}</span>
                            ) : (
                              <span className="text-muted detail-text">No Team Assigned</span>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className="card-footer bg-transparent border-0">
                        <button className="btn btn-sm btn-outline-primary w-100">
                          View Profile
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="col-12">
                <p className="no-data">No users found matching "{searchTerm}"</p>
              </div>
            )}
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table table-hover users-table">
              <thead>
                <tr>
                  <th scope="col">User</th>
                  <th scope="col">Email</th>
                  <th scope="col">Team</th>
                  <th scope="col">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.length > 0 ? (
                  filteredUsers.map((user) => {
                    const avatar = getAvatar(user.username);
                    return (
                      <tr key={user.id}>
                        <td>
                          <div className="d-flex align-items-center">
                            <div 
                              className="user-avatar-small me-2"
                              style={{ backgroundColor: avatar.color }}
                            >
                              {avatar.initial}
                            </div>
                            <div>
                              <strong>{user.username}</strong>
                              <br />
                              <small className="text-muted">ID: {user.id}</small>
                            </div>
                          </div>
                        </td>
                        <td>
                          <a href={`mailto:${user.email}`} className="text-decoration-none">
                            {user.email}
                          </a>
                        </td>
                        <td>
                          {user.team_name || user.team ? (
                            <span className="badge bg-primary">{user.team_name || user.team}</span>
                          ) : (
                            <span className="text-muted">No Team</span>
                          )}
                        </td>
                        <td>
                          <button className="btn btn-sm btn-outline-primary">
                            View
                          </button>
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan="4" className="no-data">No users found matching "{searchTerm}"</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Users;
