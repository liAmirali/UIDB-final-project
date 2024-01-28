CREATE TABLE IF NOT EXISTS address(
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

CREATE TABLE IF NOT EXISTS user(
	user_id INT PRIMARY KEY auto_increment,
    first_name VARCHAR(250),
    last_name VARCHAR(250),
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    address_id INT,
    role ENUM ('customer', 'manager'),
    foreign key (address_id) references address(address_id)
);

CREATE TABLE IF NOT EXISTS film(
	film_id INT PRIMARY KEY auto_increment,
    title VARCHAR(100) not null,
	description VARCHAR(250),
    release_date TIMESTAMP,
    rate INT,
    rent_cost_per_day INT default 2,
    penalty_cost_per_day INT default 3
);

CREATE TABLE IF NOT EXISTS shop(
	shop_id INT PRIMARY KEY auto_increment,
    shop_name VARCHAR(50),
    manager_id INT not null,
    address_id INT not null,
	foreign key (manager_id) references user(user_id),
	foreign key (address_id) references address(address_id)
);

CREATE TABLE IF NOT EXISTS dvd(
	dvd_id INT PRIMARY KEY auto_increment,
    film_id INT not null,
    shop_id INT not null,
    production_date TIMESTAMP,
	foreign key (film_id) references film(film_id),
	foreign key (shop_id) references shop(shop_id)
);

CREATE TABLE IF NOT EXISTS reserve(
	reserve_id INT PRIMARY KEY auto_increment,
    customer_id INT not null,
    dvd_id INT not null,
    created_at timestamp not null default current_timestamp,
    accepted BOOLEAN DEFAULT NULL,
    check_date timestamp default null,
    foreign key (customer_id) references user(user_id),
	foreign key (dvd_id) references dvd(dvd_id)
);

CREATE TABLE IF NOT EXISTS rental(
	rental_id INT PRIMARY KEY auto_increment,
    customer_id INT not null,
    dvd_id INT not null,
    rental_date TIMESTAMP NULL DEFAULT NULL,
	due_date TIMESTAMP NULL DEFAULT NULL,
    return_date TIMESTAMP NULL DEFAULT NULL,
    status ENUM("checking", "rejected", "accepted") DEFAULT "checking",
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    foreign key (customer_id) references user(user_id),
	foreign key (dvd_id) references dvd(dvd_id)
);

CREATE TABLE IF NOT EXISTS payment(
	payment_id INT PRIMARY KEY auto_increment,
    rental_id INT not null,
    payment_date timestamp not null,
    amount INT not null,
    foreign key (rental_id) references rental(rental_id)
);

CREATE TABLE IF NOT EXISTS actor(
	actor_id INT PRIMARY KEY auto_increment,
    first_name VARCHAR(20),
    last_name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS plays(
	film_id INT not null,
    actor_id INT not null,
    PRIMARY KEY (film_id, actor_id),
    foreign key (film_id) references film(film_id),
    foreign key (actor_id) references actor(actor_id)
);

CREATE TABLE IF NOT EXISTS category(
	category_id INT PRIMARY KEY auto_increment,
    category_name VARCHAR(20) not null
);

CREATE TABLE IF NOT EXISTS language(
	language_id INT PRIMARY KEY auto_increment,
    language_name VARCHAR(20) not null
);

CREATE TABLE IF NOT EXISTS film_category(
	film_id INT not null,
	category_id INT not null,
    PRIMARY KEY (film_id, category_id),
    foreign key (film_id) references film(film_id),
    foreign key (category_id) references category(category_id)
);

CREATE TABLE IF NOT EXISTS film_language(
	film_id INT not null,
	language_id INT not null,
    PRIMARY KEY (film_id, language_id),
    foreign key (film_id) references film(film_id),
    foreign key (language_id) references language(language_id)
);

-- trigger for delay condition and active rent for same dvd
DELIMITER //
CREATE TRIGGER on_before_rent_insert
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    declare delay_count int;
	declare active_rent_count int;

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

    select count(*) INTO active_rent_count
    from rental
    where dvd_id = NEW.dvd_id AND return_date is null;
	
    IF active_rent_count > 1 THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ALREADY RENTED';
    END if;
END;
//

CREATE TRIGGER check_manager_limit
BEFORE INSERT ON shop
FOR EACH ROW
BEGIN
    DECLARE shop_count INT;

    SELECT COUNT(*) INTO shop_count
    FROM shop
    WHERE manager_id = NEW.manager_id;

    IF shop_count > 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Manager cannot be assigned to more than 2 shops';
    END IF;
END;
//

CREATE TRIGGER check_rent_count_limit
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    DECLARE dvd_count INT;

    SELECT COUNT(*) INTO dvd_count
    FROM rental r
    JOIN dvd d ON r.dvd_id = d.dvd_id
    WHERE r.customer_id = NEW.customer_id
      AND d.shop_id = (SELECT shop_id FROM dvd WHERE dvd_id = NEW.dvd_id)
      AND r.return_date IS NULL;

    IF dvd_count > 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Customer cannot rent more than 3 DVDs from the same shop simultaneously';
    END IF;
END;
//

CREATE TRIGGER check_rental_duration
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(DAY, NEW.rental_date, NEW.due_date) > 14 OR TIMESTAMPDIFF(DAY, NEW.rental_date, NEW.due_date) < 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Rental duration must be between 1 and 14 days';
    END IF;
END;
//

CREATE TRIGGER active_rent_check
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    declare active_rent_count int;
    select count(*) INTO active_rent_count
    from rental
    where dvd_id = NEW.dvd_id AND return_date is null;
	
    IF active_rent_count > 1 THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'ALREADY RENTED';
    END if;
END;
//

CREATE TRIGGER no_rent_reserved
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    DECLARE reserve_accepted BOOLEAN;
    
    -- Check if the dvd_id being inserted is in reserve with accepted = true
    SELECT accepted INTO reserve_accepted 
    FROM reserve 
    WHERE dvd_id = NEW.dvd_id AND accepted = TRUE;
    
    -- If found, prevent insertion
    IF reserve_accepted THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot add DVD with accepted reservation into rental';
    END IF;
END;
//

DELIMITER ;
