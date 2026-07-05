CREATE TABLE repositories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL UNIQUE,
    last_indexed TIMESTAMP,
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);
