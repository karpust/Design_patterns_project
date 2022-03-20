PRAGMA foreign_keys = on;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS buyer;
CREATE TABLE buyer (
                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                       name VARCHAR (32)

);


DROP TABLE IF EXISTS category;
CREATE TABLE category (
                          id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                          name VARCHAR (32)

);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
                         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                         name VARCHAR (32),
                         category_id INTEGER NOT NULL,
                         FOREIGN KEY (category_id) REFERENCES category(id)

);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;