DROP DATABASE IF EXISTS music_db;
DROP USER IF EXISTS 'developer'@'localhost';

CREATE DATABASE music_db;
CREATE USER 'developer'@'localhost' IDENTIFIED BY 'developer4321';
GRANT ALL PRIVILEGES ON music_db.* TO 'developer'@'localhost';