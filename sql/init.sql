-- Schema initialization for PostgreSQL

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

-- Seed initial tasks if table is empty
INSERT INTO tasks (title, done)
SELECT 'Buy groceries', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks);

INSERT INTO tasks (title, done)
SELECT 'Read a book', TRUE
WHERE NOT EXISTS (SELECT 1 FROM tasks);

INSERT INTO tasks (title, done)
SELECT 'Write some code', FALSE
WHERE NOT EXISTS (SELECT 1 FROM tasks);
