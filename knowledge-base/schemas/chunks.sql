CREATE TABLE chunks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    repository_id INT,
    file_path TEXT NOT NULL,
    start_line INT,
    end_line INT,
    content TEXT NOT NULL,
    embedding_id INT,
    FOREIGN KEY (repository_id) REFERENCES repositories(id)
);
