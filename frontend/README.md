# Task Manager Frontend

A modern, responsive React frontend for the Task Manager application.

## Features

- 🔐 User authentication (Login/Register)
- ✅ Create, read, update, and delete tasks
- 🏷️ Task status management (Todo, In Progress, Done)
- 🎨 Modern UI with smooth animations
- 📱 Fully responsive design
- 🔄 Real-time task filtering

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **CSS3** - Styling with animations

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

### UI/UX
- Gradient background design
- Card-based task layout
- Color-coded status indicators
- Smooth animations and transitions
- Responsive grid layout
- Mobile-friendly interface

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

## Troubleshooting

### CORS Issues
Make sure the backend has CORS enabled for `http://localhost:5173`

### Connection Refused
Ensure the backend API is running on port 5000

### Token Expired
Logout and login again to refresh your token

## Development

### Hot Module Replacement (HMR)
Vite provides instant HMR - changes are reflected immediately without full page reload.

### Code Organization
- Components are organized by feature
- Each component has its own CSS file
- API calls are centralized in the services layer
- Reusable logic is extracted into custom hooks (if needed)

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is part of the Task Manager application.
