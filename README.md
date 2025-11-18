# Task Manager Project

Task Manager is a versatile application designed to manage, assign, and track the completion status of tasks for groups and individuals. It provides flexibility through both a command-line interface (CLI) for quick, powerful text-based interaction and a user-friendly web interface for visual management.

This project enables teams to efficiently track who is assigned to which task and monitor progress toward completion, ensuring accountability and clear oversight of group and personal responsibilities.


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
    pip install -r requirements.txt
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
    pip install -r requirements.txt
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