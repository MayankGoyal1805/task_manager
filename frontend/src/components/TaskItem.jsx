import { useState } from 'react';
import './TaskItem.css';

function TaskItem({ task, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleStatusChange = (newStatus) => {
    onUpdate(task.id, { status: newStatus });
  };

  const handleSave = () => {
    onUpdate(task.id, { title, description });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || '');
    setIsEditing(false);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'todo': return '#e74c3c';
      case 'in_progress': return '#f39c12';
      case 'done': return '#27ae60';
      default: return '#95a5a6';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'todo': return 'To Do';
      case 'in_progress': return 'In Progress';
      case 'done': return 'Done';
      default: return status;
    }
  };

  return (
    <div className="task-item" style={{ borderLeft: `4px solid ${getStatusColor(task.status)}` }}>
      {isEditing ? (
        <div className="task-edit-form">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="edit-input"
            placeholder="Task title"
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="edit-textarea"
            placeholder="Task description (optional)"
            rows="3"
          />
          <div className="edit-actions">
            <button onClick={handleSave} className="btn-save">Save</button>
            <button onClick={handleCancel} className="btn-cancel">Cancel</button>
          </div>
        </div>
      ) : (
        <>
          <div className="task-header">
            <h3 className="task-title">{task.title}</h3>
            <span className="task-status" style={{ backgroundColor: getStatusColor(task.status) }}>
              {getStatusLabel(task.status)}
            </span>
          </div>

          {task.description && (
            <p className="task-description">{task.description}</p>
          )}

          <div className="task-actions">
            <select
              value={task.status}
              onChange={(e) => handleStatusChange(e.target.value)}
              className="status-select"
            >
              <option value="todo">To Do</option>
              <option value="in_progress">In Progress</option>
              <option value="done">Done</option>
            </select>

            <div className="action-buttons">
              <button onClick={() => setIsEditing(true)} className="btn-edit">
                ✏️ Edit
              </button>
              <button onClick={() => onDelete(task.id)} className="btn-delete">
                🗑️ Delete
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default TaskItem;
