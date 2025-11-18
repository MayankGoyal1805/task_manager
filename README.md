# Task Manager Project

Task Manager is a versatile application designed to manage, assign, and track the completion status of tasks for groups and individuals. It provides flexibility through both a command-line interface (CLI) for quick, powerful text-based interaction and a user-friendly web interface for visual management.

This project enables teams to efficiently track who is assigned to which task and monitor progress toward completion, ensuring accountability and clear oversight of group and personal responsibilities.

## 🏛️ Architecture

This project is built using a modern 3-tier architecture, which separates the database, the core logic (API), and the user interfaces.



* **Tier 1: Database (MySQL)**: The single source of truth that stores all user and task data.
* **Tier 2: Backend API (Python & Flask)**: The "brain" of the application. It handles all business logic, user authentication, and database communication. It's the only part of the app that can talk to the database.
* **Tier 3: Clients (CLI & Web)**:
    * **Python CLI**: A command-line tool that "consumes" the API, allowing for quick, text-based task management.
    * **Web Interface (React)**: A visual, browser-based client that also consumes the same API. (Currently under development).

## ✨ Features (CLI)

* **Secure User Authentication**: Full user registration and login with secure password hashing (`bcrypt`) and session management (`JWT`).
* **Full Task CRUD**:
    * **Create** new tasks.
    * **Read** (list) all your own tasks.
    * **Update** a task's status, title, or description.
    * **Delete** tasks you no longer need.
* **Multi-User Security**: You can only see and manage the tasks that you created.

---

## 🚀 Setup and Installation

Follow these steps to get the backend API and the CLI running on your local machine.

### Prerequisites

* **Python** (3.8+)
* **MySQL Server**
* **Git**
* **Node.js & npm** (for the frontend, not required for API/CLI)

### 1. Backend API Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd task_manager_project
    ```

2.  **Navigate to the backend:**
    ```bash
    cd backend
    ```

3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/WSL
    # .\venv\Scripts\Activate.ps1   # On PowerShell
    ```

4.  **Install required libraries:**
    ```bash
    pip install Flask Flask-SQLAlchemy PyMySQL Flask-Bcrypt Flask-JWT-Extended
    ```

5.  **Set up the database:**
    * Log in to your MySQL server: `mysql -u root -p`
    * Run the schema script to create the database and tables. (Make sure you are in the *root* `task_manager_project` folder).
    ```bash
    mysql -u root -p < schema.sql
    ```

6.  **Configure the Database URI:**
    * Open `backend/app.py`.
    * Find the `DATABASE_URI` line.
    * Update the username and password to match your MySQL setup. (Remember to URL-encode any special characters in your password).
    ```python
    DATABASE_URI = 'mysql+pymysql://root:YOUR_ENCODED_PASSWORD@127.0.0.1/task_manager'
    ```

7.  **Run the API server:**
    * Make sure you are in the `backend` folder with your `(venv)` active.
    ```bash
    python app.py
    ```
    The server will be running on `http://127.0.0.1:5000`.

### 2. CLI Setup

1.  **Open a *new* terminal.** (Keep the backend server running in the first one).
2.  **Navigate to the CLI directory:**
    ```bash
    cd task_manager_project/cli
    ```
3.  **Create and activate its virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
4.  **Install required libraries:**
    ```bash
    pip install requests click
    ```
    You are now ready to use the CLI.

---

## ⌨️ How to Use the CLI

All commands are run from the `cli` directory.

### User Authentication

* **Register a new user:**
    ```bash
    python task.py register
    ```
    (You will be prompted for a username, email, and password)

* **Log in:**
    ```bash
    python task.py login
    ```
    (This saves a session token to a local `.token` file)

* **Log out:**
    ```bash
    python task.py logout
    ```
    (This deletes the local token)

### Task Management

*(You must be logged in to use these commands)*

* **List all your tasks:**
    ```bash
    python task.py task list
    ```

* **Create a new task:**
    ```bash
    python task.py task create
    ```
    (You will be prompted for a title)

* **Create a task with options:**
    ```bash
    python task.py task create -t "My new task" -d "A detailed description"
    ```

* **Update a task's status:**
    ```bash
    python task.py task update 5 --status in_progress
    ```

* **Update multiple parts of a task:**
    ```bash
    python task.py task update 5 --title "New Title" --desc "New description"
    ```

* **Delete a task (with confirmation):**
    ```bash
    python task.py task delete 5
    ```

* **Delete a task (bypassing confirmation):**
    ```bash
    python task.py task delete 5 -y
    ```