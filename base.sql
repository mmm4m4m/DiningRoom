CREATE TABLE users(
  id PRIMARY KEY,
  email VARCHAR(100)
  hashed_password VARCHAR(100)
);

CREATE TABLE clients(
  id PRIMARY KEY,
  user_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE employees(
  id PRIMARY KEY,
  user_id INTEGER,
  position VARCHAR(50) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE admins(
  id PRIMARY KEY,
  user_id INTEGER NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
  ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE products(
  id PRIMARY KEY,
  name VARCHAR(100) NOT NULL 
);

CREATE TABLE orders(
  id PRIMARY KEY,
  employee_id INTEGER,
  client_id INTEGER,
  total_price FLOAT(10,2),
  status VARCHAR(255),
  FOREIGN KEY (employee_id) REFERENCES employees(id)
  ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (client_id) REFERENCES clients(id)
  ON DELETE CASCADE ON UPDATE NO ACTION
); 

CREATE TABLE dishes(
  id PRIMARY KEY,
  name VARCHAR(255),
  description TEXT,
  price FLOAT(10,2)
);

CREATE TABLE product_dish(
  id PRIMARY KEY,
  product_id INTEGER,
  dish_id INTEGER,
  FOREIGN KEY (product_id) REFERENCES products(id)
  ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (dish_id) REFERENCES dishes(id)
  ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE records(
  id PRIMARY KEY,
  admin_id INTEGER,
  title VARCHAR(255),
  description TEXT,
  FOREIGN KEY (admin_id) REFERENCES admins(id)
  ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE supplies(
  id PRIMARY KEY, 
  admin_id INTEGER,
  date DATE,
  FOREIGN KEY (admin_id) REFERENCES admins(id)
  ON DELETE CASCADE ON UPDATE NO ACTION
);

CREATE TABLE supply_product (
  id PRIMARY KEY,
  supply_id INTEGER,
  product_id INTEGER,
  price FLOAT(10,2),
  quantity INTEGER,
  FOREIGN KEY (supply_id) REFERENCES supplies(id)
  ON DELETE CASCADE ON UPDATE NO ACTION,
  FOREIGN KEY (admin_id) REFERENCES admins(id)
  ON DELETE CASCADE ON UPDATE NO ACTION
);
