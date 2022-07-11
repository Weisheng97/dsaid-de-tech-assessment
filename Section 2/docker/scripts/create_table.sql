
CREATE TABLE IF NOT EXISTS salesperson
(
    salesperson_id INT GENERATED ALWAYS AS IDENTITY,
    salesperson_name VARCHAR(100) NOT NULL,
    salesperson_phone VARCHAR(15) NOT NULL,
    PRIMARY KEY(salesperson_id)
);


CREATE TABLE IF NOT EXISTS manufacturers
(
    manufacturer_id INT GENERATED ALWAYS AS IDENTITY,
    manufacturer_name VARCHAR(50) NOT NULL,
    manufacturer_phone VARCHAR(15) NOT NULL,
    PRIMARY KEY(manufacturer_id)
);

CREATE TABLE IF NOT EXISTS customers
(
    customer_id INT GENERATED ALWAYS AS IDENTITY,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(15) NOT NULL,
    PRIMARY KEY(customer_id)
);


CREATE TABLE IF NOT EXISTS cars
(
    serial_number INT GENERATED ALWAYS AS IDENTITY,
    model_name VARCHAR(50) NOT NULL,
    manufacturer_id INT NOT NULL REFERENCES manufacturers(manufacturer_id),
    total_weight NUMERIC(15,2),
    price NUMERIC(15,2) NOT NULL,
    car_for_sale boolean NOT NULL,
    PRIMARY KEY(serial_number)
);

CREATE TABLE IF NOT EXISTS transactions
(
    transaction_id INT GENERATED ALWAYS AS IDENTITY,
    salesperson_id INT NOT NULL REFERENCES salesperson(salesperson_id),
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(15) NOT NULL,
    serial_number INT NOT NULL REFERENCES cars(serial_number),
    model_name VARCHAR(100) NOT NULL,
    manufacturer_id INT NOT NULL REFERENCES manufacturers(manufacturer_id),
    total_weight NUMERIC(15,2),
    price NUMERIC(15,2) NOT NULL,
    date_time timestamp without time zone NOT NULL,
    PRIMARY KEY(transaction_id)
);

