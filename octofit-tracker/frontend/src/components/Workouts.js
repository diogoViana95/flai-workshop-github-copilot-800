import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
      console.log('Fetching workouts from:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Workouts data received:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) return (
    <div className="loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading workouts...</p>
    </div>
  );
  
  if (error) return (
    <div className="error-container">
      <h4>⚠️ Error Loading Workouts</h4>
      <p>{error}</p>
      <button className="btn btn-outline-danger" onClick={() => window.location.reload()}>Retry</button>
    </div>
  );

  const getDifficultyBadge = (level) => {
    const badges = {
      'beginner': 'bg-success',
      'intermediate': 'bg-warning',
      'advanced': 'bg-danger'
    };
    return badges[level?.toLowerCase()] || 'bg-secondary';
  };

  return (
    <div className="container mt-4">
      <div className="component-header">
        <h2>💪 Workout Suggestions</h2>
        <p className="text-muted mb-0">Personalized workout plans for your fitness goals</p>
      </div>
      <div className="p-4 bg-white rounded-bottom shadow-sm">
        <div className="row">
          {workouts.length > 0 ? (
            workouts.map((workout) => (
              <div key={workout.id} className="col-md-6 mb-4">
                <div className="card h-100">
                  <div className="card-body d-flex flex-column">
                    <h5 className="card-title">💪 {workout.name}</h5>
                    <p className="card-text flex-grow-1">{workout.description}</p>
                    <div className="mt-auto">
                      <div className="mb-2">
                        <span className="badge bg-info me-2">{workout.workout_type}</span>
                        <span className="badge bg-primary me-2">{workout.duration} min</span>
                        <span className={`badge ${getDifficultyBadge(workout.difficulty_level)}`}>
                          {workout.difficulty_level}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="card-footer bg-transparent border-0">
                    <button className="btn btn-sm btn-primary w-100">Start Workout</button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="col-12">
              <p className="no-data">No workouts found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Workouts;
