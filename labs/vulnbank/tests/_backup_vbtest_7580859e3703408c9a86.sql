-- VulnBank lab export (intentionally exposed via /backup)
SET NAMES utf8mb4;
INSERT INTO users (username, role, email, secret_note) VALUES ('admin','admin','admin@seclab.local','FLAG{admin_secret_note_found}');
INSERT INTO users (username, role, email, secret_note) VALUES ('user1','user','user1@seclab.local','My personal secret');
INSERT INTO users (username, role, email, secret_note) VALUES ('user2','user','user2@seclab.local','Card Number: 4111-1111-1111-1111');
INSERT INTO users (username, role, email, secret_note) VALUES ('bob','user','bob@seclab.local','FLAG{idor_user_data_exposed}');
