CREATE TABLE address(
	address_id INT PRIMARY KEY auto_increment,
    address VARCHAR(250),
    address2 VARCHAR(250),
    district VARCHAR(50),
    postal_code VARCHAR(20),
    phone VARCHAR(20),
    location VARCHAR(50),
    city VARCHAR(20),
    country VARCHAR(20)
);

CREATE TABLE user(
	user_id INT PRIMARY KEY auto_increment,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    email VARCHAR(20),
    address_id INT,
    role ENUM ('customer', 'manager'),
    foreign key (address_id) references address(address_id)
);

CREATE TABLE film(
	film_id INT PRIMARY KEY auto_increment,
    title VARCHAR(100) not null,
	description VARCHAR(250),
    release_date TIMESTAMP,
    rate INT,
    rent_cost_per_day INT default 2,
    penalty_cost_per_day INT default 3
);

CREATE TABLE shop(
	shop_id INT PRIMARY KEY auto_increment,
    shop_name VARCHAR(50),
    manager_id INT not null,
    address_id INT not null,
	foreign key (manager_id) references user(user_id),
	foreign key (address_id) references address(address_id),
    CONSTRAINT check_manager_limit CHECK (NOT EXISTS
        (SELECT manager_id, count(shop_id) as shop_cnt
        FROM shop
        GROUP BY manager_id
        HAVING shop_cnt > 2;))
);

CREATE TABLE dvd(
	dvd_id INT PRIMARY KEY auto_increment,
    film_id INT not null,
    shop_id INT not null,
    production_date TIMESTAMP,
	foreign key (film_id) references film(film_id),
	foreign key (shop_id) references shop(shop_id)
);

CREATE TABLE reserve_req(
	reserve_id INT PRIMARY KEY auto_increment,
    customer_id INT not null,
    dvd_id INT not null,
    creation_date timestamp not null default current_timestamp,
    accepted BOOLEAN DEFAULT FALSE,
    check_date timestamp default null,
    foreign key (customer_id) references user(user_id),
	foreign key (dvd_id) references dvd(dvd_id)
);

CREATE TABLE rental(
	rental_id INT PRIMARY KEY auto_increment,
    customer_id INT not null,
    dvd_id INT not null,
    rental_date TIMESTAMP not null,
    return_date TIMESTAMP NULL default null,
	due_date TIMESTAMP,
    accepted BOOLEAN DEFAULT FALSE,
    check_date TIMESTAMP NULL default null,
    foreign key (customer_id) references user(user_id),
	foreign key (dvd_id) references dvd(dvd_id),
    CONSTRAINT check_rent_count_limit CHECK (NOT EXISTS
        (SELECT customer_id, shop_id, count(dvd_id) as dvd_cnt
        FROM rental JOIN dvd USING (dvd_id)
        WHERE return_date IS NULL
        GROUP BY customer_id, shop_id
        HAVING dvd_cnt > 3)),
    CONSTRAINT check_rental_duration CHECK (NOT EXISTS
        (SELECT rental_id FROM rental
        WHERE TIMESTAMPDIFF(DAY, rental_date, due_date) > 14
        OR TIMESTAMPDIFF(DAY, rental_date, due_date) < 1));
);

CREATE TABLE payment(
	payment_id INT PRIMARY KEY auto_increment,
    rental_id INT not null,
    payment_date timestamp not null,
    amount INT not null,
    foreign key (rental_id) references rental(rental_id)
);

CREATE TABLE actor(
	actor_id INT PRIMARY KEY auto_increment,
    first_name VARCHAR(20),
    last_name VARCHAR(20)
);

CREATE TABLE plays(
	film_id INT not null,
    actor_id INT not null,
    PRIMARY KEY (film_id, actor_id),
    foreign key (film_id) references film(film_id),
    foreign key (actor_id) references actor(actor_id)
);

CREATE TABLE category(
	category_id INT PRIMARY KEY auto_increment,
    category_name VARCHAR(20) not null
);

CREATE TABLE language(
	language_id INT PRIMARY KEY auto_increment,
    language_name VARCHAR(20) not null
);

CREATE TABLE film_category(
	film_id INT not null,
	category_id INT not null,
    PRIMARY KEY (film_id, category_id),
    foreign key (film_id) references film(film_id),
    foreign key (category_id) references category(category_id)
);

CREATE TABLE film_language(
	film_id INT not null,
	language_id INT not null,
    PRIMARY KEY (film_id, language_id),
    foreign key (film_id) references film(film_id),
    foreign key (language_id) references language(language_id)
);

-- trigger for delay condition
DELIMITER //
CREATE TRIGGER check_customer_delay
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    declare delay_count int;

    SELECT COUNT(*) INTO delay_count
    FROM rental
    WHERE customer_id = NEW.customer_id 
    AND (
        (return_date IS NULL AND NOW() > due_date) 
        OR 
        (return_date IS NOT NULL AND return_date > due_date)
    );

    IF delay_count > 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'TOO MANY DELAYS FOR THIS CUSTOMER';
    END IF;
END;
//

DELIMITER ;
