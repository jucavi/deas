DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS dea;


CREATE TABLE user (
    id TEXT PRIMARY KEY UNIQUE,
    email TEXT,
    password TEXT,
    token TEXT
);

CREATE TABLE dea (
    id TEXT PRIMARY KEY UNIQUE,
    name TEXT,
    address TEXT,
    x INTEGER,
    y INTEGER
);
