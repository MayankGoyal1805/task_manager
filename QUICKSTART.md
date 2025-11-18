# Task Manager - Quick Start Guide

## Running the Complete Application

### 1. Start the Backend API
```bash
cd backend
source myenv/bin/activate  # or venv/bin/activate
python app.py
```
✅ Backend running at: `http://127.0.0.1:5000`

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```
✅ Frontend running at: `http://localhost:5173`

### 3. (Optional) Use the CLI
```bash
cd cli
source myenv/bin/activate  # or venv/bin/activate
python task.py --help
```

## Project Structure

```
task_manager/
├── backend/          # Flask REST API
│   ├── app.py       # Main application
│   └── myenv/       # Python virtual environment
│
├── frontend/        # React Web Interface
│   ├── src/
│   │   ├── components/  # React components
│   │   └── services/    # API service layer
│   ├── package.json
│   └── vite.config.js
│
├── cli/             # Command Line Interface
│   ├── task.py      # CLI application
│   └── myenv/       # Python virtual environment
│
└── schema.sql       # Database schema
```

## Common Commands

### Frontend Development
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### CLI Usage
```bash
# Authentication
python task.py register
python task.py login
python task.py logout

# Task Management
python task.py task list
python task.py task create -t "Task title" -d "Description"
python task.py task update <id> --status in_progress
python task.py task delete <id>
```

### Backend
```bash
# Run in debug mode
python app.py

# The API will be available at http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | Register new user |
| POST | /api/login | Login user |
| GET | /api/tasks | Get all user tasks |
| POST | /api/tasks | Create new task |
| PUT | /api/tasks/:id | Update task |
| DELETE | /api/tasks/:id | Delete task |

