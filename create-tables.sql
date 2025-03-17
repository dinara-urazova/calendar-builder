CREATE DATABASE calendar_builder;

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    base_type VARCHAR(50) NOT NULL
);

