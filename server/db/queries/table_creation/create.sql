CREATE TABLE user(
	user_id INT PRIMARY KEY auto_increment,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL,
    email VARCHAR(20),
    address_id INT,
    role ENUM ('costumer', 'manager')
);


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

CREATE TABLE reserve_req(
	reserve_id INT PRIMARY KEY auto_increment,
    costumer_id INT not null,
    dvd_id INT not null,
    creation_date timestamp not null default current_timestamp,
    accepted BOOLEAN DEFAULT FALSE,
    check_date timestamp default null,
    foreign key (costumer_id) references user(user_id),
	foreign key (dvd_id) references dvd(dvd_id)
);

CREATE TABLE rental(
	rental_id INT PRIMARY KEY auto_increment,
    costumer_id INT not null,
    dvd_id INT not null,
    renrtal_date timestamp,
    return_date timestamp default null,
	due_date timestamp,
    accepted BOOLEAN DEFAULT FALSE,
    check_date timestamp default null,
    foreign key (costumer_id) references user(user_id),
	foreign key (dvd_id) references dvd(dvd_id)
);

CREATE TABLE payment(
	payment_id INT PRIMARY KEY auto_increment,
    rental_id INT not null,
    payment_date timestamp not null,
    amount INT not null,
    foreign key (rental_id) references rental(rental_id)
);

CREATE TABLE shop(
	shop_id INT PRIMARY KEY auto_increment,
    shop_name VARCHAR(50),
    manager_id INT not null,
    address_id INT not null,
	foreign key (manager_id) references user(user_id),
	foreign key (address_id) references address(address_id)
);

CREATE TABLE dvd(
	dvd_id INT PRIMARY KEY auto_increment,
    film_id INT not null,
    shop_id INT not null,
    production_date date,
	foreign key (film_id) references film(film_id),
	foreign key (shop_id) references shop(shop_id)
);

CREATE TABLE film(
	film_id INT PRIMARY KEY auto_increment,
    title VARCHAR(100) not null,
	description VARCHAR(250),
    release_date DATE,
    rate INT,
    rent_cost_per_day INT default 2,
    penalty_cost_per_day INT default 3
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