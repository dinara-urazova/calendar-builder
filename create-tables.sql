CREATE DATABASE calendar_builder;

CREATE TABLE IF NOT EXISTS events (
    -- id SERIAL PRIMARY KEY,
    date DATE NOT NULL PRIMARY KEY,
    stars INT NULL DEFAULT NULL,
    base_types VARCHAR(50) NOT NULL,
    holiday VARCHAR NULL DEFAULT NULL,
    
);


id  date        stars  base_types holiday
1   2025-04-29  3      "tl,a"        Лосар

