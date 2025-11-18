DROP DATABASE IF EXISTS task_manager;

CREATE DATABASE task_manager;
USE task_manager;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE INDEX `idx_username_unique` (username ASC),
  UNIQUE INDEX `idx_email_unique` (email ASC)
);
  

CREATE TABLE tasks (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  description TEXT NULL, -- Description can be optional (NULL)
  status ENUM('todo', 'in_progress', 'done') NOT NULL DEFAULT 'todo',
  due_date DATE NULL, -- Due date is also optional
  creator_id INT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),


  INDEX `fk_tasks_users_idx` (creator_id ASC),
  CONSTRAINT `fk_tasks_users`
    FOREIGN KEY (creator_id)
    REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);


CREATE TABLE task_assignments (
  user_id INT NOT NULL,
  task_id INT NOT NULL,
  
  -- The Primary Key is the *combination* of both IDs.
  -- This prevents a user from being assigned to the same task twice.
  PRIMARY KEY (user_id, task_id),
  
  INDEX `fk_assignments_users_idx` (user_id ASC),
  CONSTRAINT `fk_assignments_users`
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,

  INDEX `fk_assignments_tasks_idx` (task_id ASC),
  CONSTRAINT `fk_assignments_tasks`
    FOREIGN KEY (task_id)
    REFERENCES tasks(id)
    ON DELETE CASCADE
    ON UPDATE NO ACTION
);