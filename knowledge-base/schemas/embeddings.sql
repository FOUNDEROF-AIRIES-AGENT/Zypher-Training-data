CREATE TABLE embeddings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    chunk_id INT,
    vector BLOB NOT NULL,
    model_version VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chunk_id) REFERENCES chunks(id)
);
