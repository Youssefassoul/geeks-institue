CREATE DATABASE public;

-- Create tables
CREATE TABLE IF NOT EXISTS items (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL,
  price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL
);

-- Insert items
INSERT INTO items (name, price) VALUES
  ('Small Desk', 100),
  ('Large desk', 300),
  ('Fan', 80);

-- Insert customers
INSERT INTO customers (first_name, last_name) VALUES
  ('Greg', 'Jones'),
  ('Sandra', 'Jones'),
  ('Scott', 'Scott'),
  ('Trevor', 'Green'),
  ('Melanie', 'Johnson');

-- Queries
-- 1) All the items
SELECT * FROM items;

-- 2) All the items with a price above 80 (80 not included)
SELECT * FROM items WHERE price > 80;

-- 3) All the items with a price below 300 (300 included)
SELECT * FROM items WHERE price <= 300;

-- 4) All customers whose last name is 'Smith'
-- Outcome: returns 0 rows with current data
SELECT * FROM customers WHERE last_name = 'Smith';

-- 5) All customers whose last name is 'Jones'
SELECT * FROM customers WHERE last_name = 'Jones';

-- 6) All customers whose firstname is not 'Scott'
SELECT * FROM customers WHERE first_name <> 'Scott';


