import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { taskAPI, authAPI } from '../services/api';
import TaskForm from './TaskForm';
import TaskItem from './TaskItem';
import './TaskList.css';

function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('all');
  const navigate = useNavigate();

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await taskAPI.getTasks();
      setTasks(data);
      setError('');
    } catch (err) {
      if (err.response?.status === 401) {
        authAPI.logout();
        navigate('/login');
      } else {
        setError('Failed to fetch tasks');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (title, description) => {
    try {
      await taskAPI.createTask(title, description);
      setShowForm(false);
      await fetchTasks();
    } catch (err) {
      setError('Failed to create task');
    }
  };

  const handleUpdateTask = async (taskId, updates) => {
    try {
      await taskAPI.updateTask(taskId, updates);
      await fetchTasks();
    } catch (err) {
      setError('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskAPI.deleteTask(taskId);
        await fetchTasks();
      } catch (err) {
        setError('Failed to delete task');
      }
    }
  };

  const handleLogout = () => {
    authAPI.logout();
    navigate('/login');
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    return task.status === filter;
  });

  const taskCounts = {
    all: tasks.length,
    todo: tasks.filter(t => t.status === 'todo').length,
    in_progress: tasks.filter(t => t.status === 'in_progress').length,
    done: tasks.filter(t => t.status === 'done').length,
  };

  return (
    <div className="task-list-container">
      <header className="task-header">
        <h1>My Tasks</h1>
        <button onClick={handleLogout} className="btn-logout">
          Logout
        </button>
      </header>

      {error && <div className="error-message">{error}</div>}

      <div className="task-controls">
        <div className="filter-buttons">
          <button
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All ({taskCounts.all})
          </button>
          <button
            className={`filter-btn ${filter === 'todo' ? 'active' : ''}`}
            onClick={() => setFilter('todo')}
          >
            To Do ({taskCounts.todo})
          </button>
          <button
            className={`filter-btn ${filter === 'in_progress' ? 'active' : ''}`}
            onClick={() => setFilter('in_progress')}
          >
            In Progress ({taskCounts.in_progress})
          </button>
          <button
            className={`filter-btn ${filter === 'done' ? 'active' : ''}`}
            onClick={() => setFilter('done')}
          >
            Done ({taskCounts.done})
          </button>
        </div>

        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary"
        >
          {showForm ? 'Cancel' : '+ New Task'}
        </button>
      </div>

      {showForm && (
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowForm(false)}
        />
      )}

      {loading ? (
        <div className="loading">Loading tasks...</div>
      ) : filteredTasks.length === 0 ? (
        <div className="no-tasks">
          <p>No tasks found. Create your first task!</p>
        </div>
      ) : (
        <div className="tasks-grid">
          {filteredTasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onUpdate={handleUpdateTask}
              onDelete={handleDeleteTask}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default TaskList;
