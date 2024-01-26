CREATE TABLE user(
	user_id INT PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20),
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    email VARCHAR(20),
    address_id INT
);

CREATE TABLE manager(
	manager_id INT PRIMARY KEY
);

CREATE TABLE costumer(
	costumer_id INT PRIMARY KEY
);

CREATE TABLE address(
	address_id INT PRIMARY KEY,
    address VARCHAR(50),
    address2 VARCHAR(50),
    district VARCHAR(50),
    postal_code VARCHAR(20),
    phone VARCHAR(20),
    location VARCHAR(50),
    city VARCHAR(20),
    country VARCHAR(20)
);

CREATE TABLE address(
	address_id INT PRIMARY KEY,
    address VARCHAR(50),
    address2 VARCHAR(50),
    district VARCHAR(50),
    postal_code VARCHAR(20),
    phone VARCHAR(20),
    location VARCHAR(50),
    city VARCHAR(20),
    country VARCHAR(20)
);

CREATE TABLE reserve_req(
	reserve_id INT,
    costumer_id INT,
    dvd_id INT,
    creation_date DATE,
    accepted BOOLEAN DEFAULT FALSE,
    check_date DATE,
    PRIMARY KEY (reserve_id, costumer_id, dvd_id)
);

CREATE TABLE rental(
	rental_id INT,
    costumer_id INT,
    dvd_id INT,
    renrtal_date DATE,
    return_date DATE,
	due_date DATE,
    accepted BOOLEAN DEFAULT FALSE,
    check_date DATE,
    PRIMARY KEY (rental_id, costumer_id, dvd_id)
);

CREATE TABLE payment(
	payment_id INT,
    rental_id INT,
    payment_date DATE,
    amount INT,
    PRIMARY KEY (payment_id, rental_id)
);

CREATE TABLE shop(
	shop_id INT PRIMARY KEY,
    shop_name VARCHAR(20),
    manager_id INT,
    address_id INT
);

CREATE TABLE dvd(
	dvd_id INT PRIMARY KEY,
    film_id INT,
    shop_id INT,
    production_date DATE
);

CREATE TABLE film(
	film_id INT PRIMARY KEY,
    title VARCHAR(50),
	description VARCHAR(100),
    release_date DATE,
    rental_duration INT,
    rate INT,
    rent_cost_per_day INT,
    penalty_cost_per_day INT
);

CREATE TABLE actor(
	actor_id INT PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20)
);


CREATE TABLE plays(
	film_id INT,
    actor_id INT,
    PRIMARY KEY (film_id, actor_id)
);

CREATE TABLE category(
	category_id INT PRIMARY KEY,
    category_name VARCHAR(20)
);

CREATE TABLE language(
	language_id INT PRIMARY KEY,
    language_name VARCHAR(20)
);

CREATE TABLE film_category(
	film_id INT,
	category_id INT,
    PRIMARY KEY (film_id, category_id)
);

CREATE TABLE film_language(
	film_id INT,
	language_id INT,
    PRIMARY KEY (film_id, language_id)
);












