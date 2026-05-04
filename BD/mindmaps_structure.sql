CREATE SCHEMA mindmaps;

USE mindmaps;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pseudo VARCHAR(100) NOT NULL UNIQUE,
    hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE maps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (author_id) REFERENCES users(id)
);

CREATE TABLE nodes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    
    map_id INT NOT NULL,              -- la mind-map à laquelle appartient le nœud
    parent_id INT DEFAULT NULL,       -- nœud parent (NULL = racine)
    
    author_id INT NOT NULL,           -- créateur du nœud
    text TEXT NOT NULL,               -- contenu du nœud
    
    level INT NOT NULL DEFAULT 0,     -- niveau hiérarchique (optimisation)  
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (map_id) REFERENCES maps(id),
    FOREIGN KEY (parent_id) REFERENCES nodes(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id)
);