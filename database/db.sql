CREATE DATABASE saas_platform;

USE saas_platform;

-- Tabela Prestador
CREATE TABLE provider (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    specialty VARCHAR(100),
    description TEXT,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

-- Tabela Cliente
CREATE TABLE client (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    preference1 VARCHAR(100),
    preference2 VARCHAR(100),
    preference3 VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

-- Tabela Categoria
CREATE TABLE category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Tabela Avaliações
CREATE TABLE review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    provider_id INT,
    client_id INT,
    rating INT CHECK(rating BETWEEN 1 AND 5),
    comment TEXT,
    FOREIGN KEY (provider_id) REFERENCES provider(id),
    FOREIGN KEY (client_id) REFERENCES client(id)
);

-- Tabela Pagamento Cliente
CREATE TABLE client_payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    amount DECIMAL(10,2),
    payment_date DATE,
    FOREIGN KEY (client_id) REFERENCES client(id)
);

-- Tabela Pagamento Prestador
CREATE TABLE provider_payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    provider_id INT,
    amount DECIMAL(10,2),
    payment_date DATE,
    FOREIGN KEY (provider_id) REFERENCES provider(id)
);
GRANT ALL PRIVILEGES ON *.* TO root IDENTIFIED BY senai@123;
FLUSH PRIVILEGES;
