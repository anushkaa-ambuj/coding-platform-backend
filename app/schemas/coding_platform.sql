-- Users table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY, -- UUID stored as a 36-character string
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'candidate') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Challenges table
CREATE TABLE challenges (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    time_limit INT NOT NULL CHECK (time_limit > 0),
    memory_limit INT NOT NULL CHECK (memory_limit > 0),
    created_by CHAR(36) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Public test cases
CREATE TABLE public_test_cases (
    id CHAR(36) PRIMARY KEY,
    challenge_id CHAR(36) NOT NULL,
    input TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE
);

-- Hidden test cases
CREATE TABLE hidden_test_cases (
    id CHAR(36) PRIMARY KEY,
    challenge_id CHAR(36) NOT NULL,
    s3_input_path VARCHAR(255) NOT NULL,
    s3_output_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE
);

-- Submissions
CREATE TABLE submissions (
    id CHAR(36) PRIMARY KEY,
    challenge_id CHAR(36) NOT NULL,
    user_id CHAR(36) NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed') NOT NULL,
    language_id INT NOT NULL,
    score FLOAT,
    execution_time FLOAT,
    memory_used FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
