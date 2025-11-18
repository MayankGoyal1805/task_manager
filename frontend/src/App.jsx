import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { authAPI } from './services/api';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import TaskList from './components/TaskList';
import './App.css';

// Protected Route component
function ProtectedRoute({ children }) {
  const isAuthenticated = authAPI.isAuthenticated();
  return isAuthenticated ? children : <Navigate to="/login" />;
}

// Public Route component (redirect to tasks if already logged in)
function PublicRoute({ children }) {
  const isAuthenticated = authAPI.isAuthenticated();
  return !isAuthenticated ? children : <Navigate to="/tasks" />;
}

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route
            path="/"
            element={
              authAPI.isAuthenticated() ? <Navigate to="/tasks" /> : <Home />
            }
          />
          
          <Route
            path="/login"
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            }
          />
          
          <Route
            path="/register"
            element={
              <PublicRoute>
                <Register />
              </PublicRoute>
            }
          />
          
          <Route
            path="/tasks"
            element={
              <ProtectedRoute>
                <TaskList />
              </ProtectedRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
