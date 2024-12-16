DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    flag TEXT
);

INSERT INTO users (username, password, role) VALUES ('user', 'password', 'user');
INSERT INTO users (username, password, role, flag) VALUES ('admin', 'adminpass', 'admin', 'CTF{SQLi_Exploited}');
