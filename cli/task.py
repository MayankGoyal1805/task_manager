import requests
import click
import os

# --- Configuration ---
CLI_DIR = os.path.dirname(os.path.realpath(__file__))
TOKEN_FILE = os.path.join(CLI_DIR, ".token")
API_URL = "http://127.0.0.1:5000"

# --- Helper Functions ---
def style_error(text):
    return click.style(text, fg="red")

def style_success(text):
    return click.style(text, fg="green")

def get_auth_headers():
    """Reads the token and builds the authorization header."""
    if not os.path.exists(TOKEN_FILE):
        return None
    
    with open(TOKEN_FILE, 'r') as f:
        token = f.read().strip()
        
    if not token:
        return None
        
    return {
        "Authorization": f"Bearer {token}"
    }


# --- MAIN 'cli' GROUP ---
@click.group()
def cli():
    """A CLI for the Task Manager API"""
    pass

# --- 'register' Command ---
@cli.command()
@click.option('--username', prompt=True)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
def register(username, email, password):
    """Registers a new user"""
    payload = {
        'username': username,
        'email': email,
        'password': password
    }
    try:
        response = requests.post(f"{API_URL}/api/register", json=payload)
        response.raise_for_status()
        data = response.json()
        click.echo(style_success(f"{data['message']} (ID: {data['user_id']})"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_data = e.response.json()
            click.echo(style_error(f"Registration failed: {error_data.get('error')}"))
        else:
            click.echo(style_error(f"An error occurred: {e}"))
    except requests.exceptions.ConnectionError:
        click.echo(style_error("Error: Could not connect to the API."))
    except Exception as e:
        click.echo(style_error(f"An unexpected error occurred: {e}"))

# --- 'login' Command ---
@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(username, password):
    """Logs in the user and saves the auth token."""
    payload = {'username': username, 'password': password}
    try:
        response = requests.post(f"{API_URL}/api/login", json=payload)
        response.raise_for_status()
        data = response.json()
        access_token = data.get('access_token')
        with open(TOKEN_FILE, 'w') as f:
            f.write(access_token)
        click.echo(style_success("Login successful! Token saved."))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            click.echo(style_error("Login failed: Invalid username or password"))
        else:
            click.echo(style_error(f"An error occurred: {e}"))
    except requests.exceptions.ConnectionError:
        click.echo(style_error("Error: Could not connect to the API."))
    except Exception as e:
        click.echo(style_error(f"An unexpected error occurred: {e}"))

# --- 'logout' Command ---
@cli.command()
def logout():
    """Logs out the user by deleting the auth token."""
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        click.echo(style_success("Logged out successfully."))
    else:
        click.echo("You are not logged in.")

# --- 'task' Sub-group ---
@cli.group()
def task():
    """Commands for managing tasks"""
    pass

# --- 'task list' Command ---
@task.command(name="list")
def list_tasks():
    """Lists all your tasks"""
    headers = get_auth_headers()
    if not headers:
        click.echo(style_error("You must be logged in. Run 'python task.py login'"))
        return
    try:
        response = requests.get(f"{API_URL}/api/tasks", headers=headers)
        response.raise_for_status()
        data = response.json()
        tasks = data.get('tasks')
        if not tasks:
            click.echo("No tasks found.")
            return
        click.echo(f"--- Found {len(tasks)} task(s) ---")
        for t in tasks:
            click.echo(
                click.style(f"ID: {t['id']}", fg="cyan") +
                f" | Status: {t['status']}" +
                f" | Title: {t['title']}"
            )
            if t['description']:
                click.echo(f"   Desc: {t['description']}")
            click.echo("-" * 20) 
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            click.echo(style_error("Login failed or token expired. Please log in again."))
        else:
            click.echo(style_error(f"An error occurred: {e}"))
    except requests.exceptions.ConnectionError:
        click.echo(style_error("Error: Could not connect to the API."))
    except Exception as e:
        click.echo(style_error(f"An unexpected error occurred: {e}"))

# --- 'task create' Command ---
@task.command(name="create")
@click.option('--title', '-t', prompt="Task Title", help="The title of the task.")
@click.option('--desc', '-d', default="", help="The description of the task (optional).")
def create_task(title, desc):
    """Creates a new task"""
    headers = get_auth_headers()
    if not headers:
        click.echo(style_error("You must be logged in. Run 'python task.py login'"))
        return
    payload = {'title': title, 'description': desc}
    try:
        response = requests.post(f"{API_URL}/api/tasks", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        click.echo(style_success(f"Success: {data['message']} (ID: {data['task_id']})"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            click.echo(style_error("Login failed or token expired. Please log in again."))
        else:
            click.echo(style_error(f"An error occurred: {e}"))
    except requests.exceptions.ConnectionError:
        click.echo(style_error("Error: Could not connect to the API."))
    except Exception as e:
        click.echo(style_error(f"An unexpected error occurred: {e}"))

# --- 'task update' Command ---
@task.command(name="update")
@click.argument('task_id', type=int)
@click.option('--status', type=click.Choice(['todo', 'in_progress', 'done'], case_sensitive=False), help="New status.")
@click.option('--title', help="New title for the task.")
@click.option('--desc', help="New description for the task.")
def update_task(task_id, status, title, desc):
    """Updates a specific task by its ID."""
    headers = get_auth_headers()
    if not headers:
        click.echo(style_error("You must be logged in. Run 'python task.py login'"))
        return
    payload = {}
    if status: payload['status'] = status
    if title: payload['title'] = title
    if desc: payload['description'] = desc
    if not payload:
        click.echo("Nothing to update! Provide --status, --title, or --desc.")
        return
    try:
        response = requests.put(f"{API_URL}/api/tasks/{task_id}", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        click.echo(style_success(f"Success: {data['message']} (ID: {data['task_id']})"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            click.echo(style_error("Login failed or token expired. Please log in again."))
        elif e.response.status_code == 403:
            click.echo(style_error("Error: You do not have permission to update this task."))
        elif e.response.status_code == 404:
            click.echo(style_error(f"Error: Task with ID {task_id} not found."))
        else:
            click.echo(style_error(f"An error occurred: {e}"))
    except requests.exceptions.ConnectionError:
        click.echo(style_error("Error: Could not connect to the API."))
    except Exception as e:
        click.echo(style_error(f"An unexpected error occurred: {e}"))

# --- 'task delete' Command ---
@task.command(name="delete")
@click.argument('task_id', type=int)
@click.option('--yes', '-y', is_flag=True, help="Bypass confirmation prompt.")
def delete_task(task_id, yes):
    """Deletes a specific task by its ID."""
    headers = get_auth_headers()
    if not headers:
        click.echo(style_error("You must be logged in. Run 'python task.py login'"))
        return
    if not yes:
        click.echo(click.style(f"Warning: You are about to delete task {task_id}.", fg="yellow"))
        if not click.confirm("Do you want to continue?"):
            click.echo("Delete operation cancelled.")
            return
    try:
        response = requests.delete(f"{API_URL}/api/tasks/{task_id}", headers=headers)
        response.raise_for_status()
        data = response.json()
        click.echo(style_success(f"Success: {data['message']}"))
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            click.echo(style_error("Login failed or token expired. Please log in again."))
        elif e.response.status_code == 403:
            click.echo(style_error("Error: You do not have permission to delete this task."))
        elif e.response.status_code == 404:
            click.echo(style_error(f"Error: Task with ID {task_id} not found."))
        else:
            click.echo(style_error(f"An error occurred: {e}"))
    except requests.exceptions.ConnectionError:
        click.echo(style_error("Error: Could not connect to the API."))
    except Exception as e:
        click.echo(style_error(f"An unexpected error occurred: {e}"))

# --- Run the main 'cli' group ---
if __name__ == '__main__':
    cli()