import { Link } from 'react-router-dom';
import './Home.css';

function Home() {
  return (
    <div className="home-container">
      <div className="home-content">
        <h1 className="home-title">Task Manager</h1>
        <p className="home-subtitle">
          Organize your tasks efficiently with our modern task management system
        </p>
        
        <div className="home-features">
          <div className="feature">
            <span className="feature-icon">✅</span>
            <h3>Easy Task Management</h3>
            <p>Create, update, and delete tasks with ease</p>
          </div>
          
          <div className="feature">
            <span className="feature-icon">🏷️</span>
            <h3>Status Tracking</h3>
            <p>Track progress with Todo, In Progress, and Done states</p>
          </div>
          
          <div className="feature">
            <span className="feature-icon">🔐</span>
            <h3>Secure & Private</h3>
            <p>Your tasks are secure with JWT authentication</p>
          </div>
        </div>

        <div className="home-actions">
          <Link to="/login" className="btn-home-primary">
            Get Started
          </Link>
          <Link to="/register" className="btn-home-secondary">
            Create Account
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
