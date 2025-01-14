CREATE DATABASE IF NOT EXISTS app_db;

USE app_db;

CREATE TABLE IF NOT EXISTS global_counter (
    counter_value INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_ip VARCHAR(45),
    internal_ip VARCHAR(45),
    access_time DATETIME
);

INSERT IGNORE INTO global_counter (counter_value) VALUES (0);