
## Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Running backend API (see `/backend` directory)

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit:
   ```
   http://localhost:5173
   ```

### Build for Production

To create a production build:

```bash
npm run build
```

The build files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── Login.jsx       # Login page
│   │   ├── Register.jsx    # Registration page
│   │   ├── TaskList.jsx    # Main task list view
│   │   ├── TaskItem.jsx    # Individual task card
│   │   ├── TaskForm.jsx    # Task creation form
│   │   └── *.css          # Component styles
│   ├── services/
│   │   └── api.js         # API service layer
│   ├── App.jsx            # Main app component
│   ├── App.css            # Global app styles
│   ├── main.jsx           # Entry point
│   └── index.css          # Global styles
├── index.html             # HTML template
├── vite.config.js         # Vite configuration
└── package.json           # Dependencies

```

## Features Detail

### Authentication
- Secure JWT-based authentication
- Token stored in localStorage
- Protected routes
- Auto-redirect for authenticated users

### Task Management
- **Create**: Add new tasks with title and optional description
- **Read**: View all your tasks with filtering options
- **Update**: Edit task details and change status
- **Delete**: Remove tasks with confirmation

### Filtering
- View all tasks
- Filter by status (Todo, In Progress, Done)
- Task count badges for each filter


## API Integration

The frontend communicates with the backend API at `http://127.0.0.1:5000/api`

### Endpoints Used:
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

## Configuration

### API URL
The API URL is configured in `src/services/api.js`:
```javascript
const API_URL = 'http://127.0.0.1:5000/api';
```

### Proxy Configuration
Vite is configured to proxy API requests in `vite.config.js`:
```javascript
proxy: {
  '/api': {
    target: 'http://127.0.0.1:5000',
    changeOrigin: true,
  }
}
```

