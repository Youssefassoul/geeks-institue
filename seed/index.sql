-- Developers table
CREATE TABLE IF NOT EXISTS developers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    founded_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Platforms table
CREATE TABLE IF NOT EXISTS platforms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    manufacturer VARCHAR(100),
    release_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Games table
CREATE TABLE IF NOT EXISTS games (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    genre VARCHAR(100) NOT NULL,
    release_year INT NOT NULL,
    rating DECIMAL(2,1),
    developer_id INT REFERENCES developers(id) ON DELETE SET NULL,
    platform_id INT REFERENCES platforms(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    game_id INT REFERENCES games(id) ON DELETE CASCADE,
    reviewer_name VARCHAR(100) NOT NULL,
    review_text TEXT NOT NULL,
    score DECIMAL(2,1) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Developers
INSERT INTO developers (name, country, founded_year)
VALUES 
('Rockstar Games', 'USA', 1998),
('CD Projekt Red', 'Poland', 2002),
('Naughty Dog', 'USA', 1984);

-- Platforms
INSERT INTO platforms (name, manufacturer, release_year)
VALUES
('PlayStation 5', 'Sony', 2020),
('Xbox Series X', 'Microsoft', 2020),
('PC', 'Various', 1980);

-- Games
INSERT INTO games (title, description, genre, release_year, rating, developer_id, platform_id)
VALUES
('The Witcher 3: Wild Hunt',
 'An open-world RPG following Geralt of Rivia, a monster hunter searching for his adopted daughter.',
 'RPG', 2015, 9.5, 2, 3),
('Grand Theft Auto V',
 'An open-world action-adventure game set in Los Santos with three playable protagonists.',
 'Action', 2013, 9.7, 1, 3),
('The Last of Us Part II',
 'A story-driven action-adventure game focusing on Ellie in a post-apocalyptic world.',
 'Action-Adventure', 2020, 9.3, 3, 1);

-- Reviews
INSERT INTO reviews (game_id, reviewer_name, review_text, score)
VALUES
(1, 'John Doe', 'Amazing RPG with a rich story and huge world!', 9.5),
(2, 'Jane Smith', 'Still one of the best open-world games ever.', 9.8),
(3, 'Alex Johnson', 'Emotional story, beautiful gameplay.', 9.2);
