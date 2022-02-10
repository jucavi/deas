DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS dea;


CREATE TABLE user (
    id TEXT PRIMARY KEY UNIQUE,
    email TEXT,
    password TEXT,
    token TEXT
);
