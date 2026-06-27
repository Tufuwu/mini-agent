MERGE INTO users (username, password_hash, role)
KEY (username)
VALUES ('admin', '$2a$10$v.8I93IUDr7R3yQbf.oem.pcy./YAAINSqOXUhpcMzQ01CnxGZyY2', 'ADMIN');
