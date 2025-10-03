-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

-- Create User Search History table
CREATE TABLE IF NOT EXISTS user_search_history (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    search_keyword VARCHAR(255) NOT NULL,
    dish_name VARCHAR(255) NOT NULL,
    calories_per_serving INT NOT NULL,
    total_calories INT NOT NULL,
    protein_per_serving INT NOT NULL,
    fat_per_serving INT NOT NULL,
    carbohydrates_per_serving INT NOT NULL,
    source VARCHAR(255),
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);