CREATE DATABASE calendar_builder;

CREATE TABLE IF NOT EXISTS events (
    date DATE NOT NULL PRIMARY KEY,
    stars INT,
    base_type VARCHAR(50),
    holiday VARCHAR(100) 
);