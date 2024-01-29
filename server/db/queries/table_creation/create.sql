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
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    address_id INT,
    role ENUM ('customer', 'manager'),
    foreign key (address_id) references address(address_id),
    UNIQUE (username),
    UNIQUE (email),
    UNIQUE (address_id)
);

CREATE TABLE IF NOT EXISTS film(
	film_id INT PRIMARY KEY auto_increment,
    title VARCHAR(100) not null,
	description VARCHAR(250),
    release_date TIMESTAMP,
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
    expired BOOLEAN DEFAULT FALSE,
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
    rate NUMERIC(2, 1) NULL DEFAULT NULL,
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    foreign key (customer_id) references user(user_id),
	foreign key (dvd_id) references dvd(dvd_id)
);

CREATE TABLE IF NOT EXISTS payment(
	payment_id INT PRIMARY KEY auto_increment,
    rental_id INT NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
CREATE TRIGGER check_maximum_delay
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    DECLARE delay_count INT;
	DECLARE active_rent_count INT;

    SELECT COUNT(*) INTO delay_count
    FROM rental
    WHERE customer_id = NEW.customer_id 
    AND (
        (status = 'accepted' AND return_date IS NULL AND NOW() > due_date) 
        OR 
        (return_date IS NOT NULL AND return_date > due_date)
    );

    IF delay_count >= 10 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Too many delays for this customer.';
    END IF;
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

    IF shop_count >= 2 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Manager cannot be assigned to more than 2 shops.';
    END IF;
END;
//

CREATE TRIGGER check_rent_count_limit
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    DECLARE active_rent_count INT;

    SELECT COUNT(*) INTO active_rent_count
    FROM rental
        JOIN dvd USING (dvd_id)
    WHERE customer_id = NEW.customer_id
        AND shop_id = (SELECT shop_id FROM dvd WHERE dvd_id = NEW.dvd_id)
        AND status='accepted' AND return_date IS NULL;

    IF active_rent_count >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Customer cannot rent more than 3 DVDs from the same shop simultaneously.';
    END IF;
END;
//

CREATE TRIGGER check_rental_duration
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    IF TIMESTAMPDIFF(DAY, NEW.rental_date, NEW.due_date) > 14 OR TIMESTAMPDIFF(DAY, NEW.rental_date, NEW.due_date) < 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Rental duration must be between 1 and 14 days.';
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
    where dvd_id = NEW.dvd_id AND status='accepted' AND return_date is null;
	
    IF active_rent_count > 0 THEN
		SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'The DVD is already rented.';
    END if;
END;
//

CREATE TRIGGER no_rent_reserved
BEFORE INSERT ON rental
FOR EACH ROW
BEGIN
    DECLARE reserve_accepted BOOLEAN;
    
    SELECT accepted INTO reserve_accepted 
    FROM reserve 
    WHERE dvd_id = NEW.dvd_id AND accepted = 1 AND expired = 0;
    
    IF reserve_accepted THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot rent a reserved DVD.';
    END IF;
END;
//

DELIMITER ;
