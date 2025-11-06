CREATE DATABASE IF NOT EXISTS ecommerce_chatbot;
USE ecommerce_chatbot;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  phone VARCHAR(30),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE addresses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  label VARCHAR(60),
  address TEXT,
  city VARCHAR(100),
  pincode VARCHAR(20),
  is_default BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE products (
  id VARCHAR(100) PRIMARY KEY,
  title VARCHAR(512),
  description TEXT,
  price DECIMAL(10,2),
  rating DECIMAL(3,2),
  image_url VARCHAR(1024),
  category VARCHAR(120)
);

INSERT INTO products (id,title,description,price,rating,image_url,category) VALUES
('P001','Nike Running Shoes','Lightweight running shoes','4999.00',4.5,'/assets/images/nike.jpg','Footwear'),
('P002','Wireless Earbuds X100','True wireless earbuds with 24h battery','1999.00',4.2,'/assets/images/earbuds.jpg','Electronics'),
('P003','Smart Fitness Band','Heart-rate monitor, sleep tracking','1299.00',4.0,'/assets/images/band.jpg','Wearables');
