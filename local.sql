create schema bio;

use bio;

CREATE TABLE IF NOT EXISTS agronomists
(
id INT auto_increment PRIMARY KEY NOT NULL,
username varchar(100) NOT NULL,
password varchar(255) NOT NULL,
first_name varchar(25) NOT NULL,
last_name varchar(25) NOT NULL,
address varchar(320) NOT NULL,
email varchar(320) NOT NULL,
phone varchar(11) NOT NULL,
date_joined date NOT NULL,
state tinyint default 1
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS staff
(
id INT auto_increment PRIMARY KEY NOT NULL,
username varchar(100) NOT NULL,
password varchar(255) NOT NULL,
first_name varchar(25) NOT NULL,
last_name varchar(25) NOT NULL,
position varchar(320) NOT NULL,
email varchar(320) NOT NULL,
phone varchar(11) NOT NULL,
date_hired date NOT NULL,
department varchar(25) NOT NULL,
state tinyint default 1
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS admin
(
id INT auto_increment PRIMARY KEY NOT NULL,
username varchar(100) NOT NULL,
password varchar(255) NOT NULL,
first_name varchar(25) NOT NULL,
last_name varchar(25) NOT NULL,
position varchar(320) NOT NULL,
email varchar(320) NOT NULL,
phone varchar(11) NOT NULL,
date_hired date NOT NULL,
department varchar(25) NOT NULL,
state tinyint default 1
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS agriculture 
(  
agriculture_id INT auto_increment PRIMARY KEY NOT NULL,
agriculture_item_type ENUM('pest', 'weed') NOT NULL,
common_name VARCHAR(255) NOT NULL,
scientific_name VARCHAR(255) NOT NULL,
key_characteristics TEXT, 
biology TEXT,
impacts TEXT,
control TEXT
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS photos 
(  
photo_id INT auto_increment PRIMARY KEY NOT NULL,  
photo_url VARCHAR(512) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS agriculture_photos 
(
agriculture_id INT,  
photo_id INT,  
is_primary BOOLEAN NOT NULL DEFAULT FALSE,  
FOREIGN KEY (agriculture_id) REFERENCES agriculture(agriculture_id),  
FOREIGN KEY (photo_id) REFERENCES photos(photo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; 

INSERT INTO admin (username, password, first_name, last_name, position, email, phone, date_hired, departmant) VALUES ('admin', '7299f3488ded4e34277fd96afcdd911449b69b111aa45f6a2bd25d168f7a87f0', 'John', 'Smith', 'New Zealand', 'admin@willis.nz', '10211661231', '2023-12-12', 'admin');