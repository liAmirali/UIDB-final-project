-- Insert data into the address table
INSERT INTO address (address, address2, district, postal_code, phone, location, city, country) VALUES
('123 Main Street', '', 'Downtown', '12345', '123-456-7890', 'New York', 'New York', 'USA'),
('456 Elm Street', 'Apt 101', 'Midtown', '54321', '987-654-3210', 'Los Angeles', 'California', 'USA'),
('789 Oak Avenue', 'Suite 201', 'Uptown', '67890', '111-222-3333', 'Chicago', 'Illinois', 'USA'),
('101 Pine Road', '', 'Suburbia', '09876', '444-555-6666', 'Houston', 'Texas', 'USA'),
('202 Maple Lane', '', 'Rural', '65432', '777-888-9999', 'Phoenix', 'Arizona', 'USA'),
('303 Cedar Drive', 'Unit 501', 'Coastal', '13579', '333-222-1111', 'Miami', 'Florida', 'USA'),
('404 Birch Court', '', 'Hills', '24680', '999-888-7777', 'Seattle', 'Washington', 'USA'),
('505 Walnut Place', 'Suite 301', 'Valley', '56789', '666-555-4444', 'San Francisco', 'California', 'USA'),
('606 Spruce Avenue', '', 'Mountains', '98765', '222-333-4444', 'Denver', 'Colorado', 'USA'),
('707 Ash Street', 'Apt 401', 'Islands', '43210', '888-999-0000', 'Honolulu', 'Hawaii', 'USA'),
("123 Main Street", "", "Downtown", "12345", "123-456-7890", "New York", "New York", "USA"),
("456 Elm Street", "Apt 101", "Midtown", "54321", "987-654-3210", "Los Angeles", "California", "USA"),
("789 Oak Avenue", "Suite 201", "Uptown", "67890", "111-222-3333", "Chicago", "Illinois", "USA"),
("101 Pine Road", "", "Suburbia", "09876", "444-555-6666", "Houston", "Texas", "USA"),
("202 Maple Lane", "", "Rural", "65432", "777-888-9999", "Phoenix", "Arizona", "USA"),
("303 Cedar Drive", "Unit 501", "Coastal", "13579", "333-222-1111", "Miami", "Florida", "USA"),
("404 Birch Court", "", "Hills", "24680", "999-888-7777", "Seattle", "Washington", "USA"),
("505 Walnut Place", "Suite 301", "Valley", "56789", "666-555-4444", "San Francisco", "California", "USA"),
("606 Spruce Avenue", "", "Mountains", "98765", "222-333-4444", "Denver", "Colorado", "USA"),
("707 Ash Street", "Apt 401", "Islands", "43210", "888-999-0000", "Honolulu", "Hawaii", "USA"),
("808 Pineapple Avenue", "Suite 501", "Beachside", "56789", "777-888-9999", "Los Angeles", "California", "USA"),
("909 Cherry Lane", "", "Downtown", "12345", "555-444-3333", "New York", "New York", "USA"),
("1010 Orange Grove", "Apt 201", "Uptown", "54321", "222-333-4444", "Chicago", "Illinois", "USA"),
("1111 Lemon Boulevard", "", "Midtown", "67890", "111-222-3333", "Houston", "Texas", "USA"),
("1212 Apple Street", "Suite 301", "Suburbia", "09876", "999-888-7777", "Phoenix", "Arizona", "USA"),
("1313 Banana Road", "", "Rural", "65432", "666-555-4444", "Miami", "Florida", "USA"),
("1414 Grape Lane", "Unit 401", "Coastal", "13579", "123-456-7890", "Seattle", "Washington", "USA"),
("1515 Mango Court", "", "Hills", "24680", "777-888-9999", "San Francisco", "California", "USA"),
("1616 Pear Place", "Apt 501", "Valley", "56789", "444-555-6666", "Denver", "Colorado", "USA"),
("1717 Watermelon Avenue", "", "Mountains", "98765", "888-999-0000", "Honolulu", "Hawaii", "USA");


-- Insert data into the user table
INSERT INTO user (first_name, last_name, username, password, email, address_id, role) VALUES
('John', 'Doe', 'johndoe', 'password1', 'john.doe@example.com', 1, 'customer'),
('Jane', 'Smith', 'janesmith', 'password2', 'jane.smith@example.com', 2, 'customer'),
('Michael', 'Johnson', 'michaelj', 'password3', 'michael.j@example.com', 3, 'manager'),
('Emily', 'Brown', 'emilyb', 'password4', 'emily.b@example.com', 4, 'customer'),
('William', 'Jones', 'willj', 'password5', 'william.j@example.com', 5, 'customer'),
('Olivia', 'Taylor', 'oliviat', 'password6', 'olivia.t@example.com', 6, 'manager'),
('James', 'Wilson', 'jamesw', 'password7', 'james.w@example.com', 7, 'customer'),
('Emma', 'Martinez', 'emmam', 'password8', 'emma.m@example.com', 8, 'customer'),
('Daniel', 'Anderson', 'danield', 'password9', 'daniel.a@example.com', 9, 'manager'),
('Sophia', 'Hernandez', 'sophiah', 'password10', 'sophia.h@example.com', 10, 'customer'),
('Asal', 'Khaef', 'asal', 'password11', 'asal.kh@example.com', 11, 'manager'),
('Amirali', 'Lotfi', 'amirali', 'password12', 'amirali.l@example.com', 12, 'manager');

-- Insert data into the film table
INSERT INTO film (title, description, release_date, rent_cost_per_day, penalty_cost_per_day) VALUES
('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', '1999-03-31', 3, 4),
('Inception', 'A thief who enters the dreams of others to steal secrets from their subconscious.', '2010-07-16', 4, 2, 3),
('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', '1994-10-14', 2, 3),
('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.', '1994-10-14', 2, 3),
('The Dark Knight', 'When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.', '2008-07-18', 2, 3),
('Fight Club', 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.', '1999-10-15', 2, 3),
('Forrest Gump', 'The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold from the perspective of an Alabama man with an IQ of 75, whose only desire is to be reunited with his childhood sweetheart.', '1994-07-06', 2, 3),
('The Godfather', 'An organized crime dynasty\'s aging patriarch transfers control of his clandestine empire to his reluctant son.', '1972-03-24', 2, 3),
('The Godfather: Part II', 'The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.', '1974-12-20', 2, 3),
('Schindler\'s List', 'In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.', '1993-12-15', 2, 3);

-- Insert data into the shop table
INSERT INTO shop (shop_name, manager_id, address_id) VALUES
('Movie Haven', 3, 1),
('Cineplex Emporium', 6, 2),
('Film Central', 9, 3),
('Blockbuster Palace', 3, 4),
('Cinema World', 6, 5),
('Flicks \'n\' Chill', 9, 6),
('Silver Screen Cinema', 11, 7),
('Theatre House', 11, 8),
('Picture Perfect', 12, 9);

-- Insert data into the dvd table
INSERT INTO dvd (film_id, shop_id, production_date) VALUES
(9, 1, "2023-01-01"),
(10, 2, "2023-01-02"),
(1, 3, "2023-01-03"),
(2, 4, "2023-01-04"),
(3, 5, "2023-01-05"),
(4, 6, "2023-01-06"),
(5, 7, "2023-01-07"),
(6, 8, "2023-01-08"),
(7, 9, "2023-01-09"),
(8, 1, "2023-01-10"),
(9, 2, "2023-01-11"),
(10, 3, "2023-01-12"),
(1, 4, "2023-01-13"),
(2, 5, "2023-01-14"),
(3, 6, "2023-01-15"),
(4, 7, "2023-01-16"),
(5, 8, "2023-01-17"),
(6, 9, "2023-01-18"),
(7, 1, "2023-01-19"),
(8, 2, "2023-01-20"),
(9, 3, "2023-01-21"),
(10, 4, "2023-01-22"),
(1, 5, "2023-01-23"),
(2, 6, "2023-01-24"),
(3, 7, "2023-01-25"),
(4, 8, "2023-01-26"),
(5, 9, "2023-01-27"),
(6, 1, "2023-01-28"),
(7, 2, "2023-01-29"),
(8, 3, "2023-01-30"),
(9, 4, "2023-01-31"),
(10, 5, "2023-02-01"),
(1, 6, "2023-02-02"),
(2, 7, "2023-02-03"),
(3, 8, "2023-02-04"),
(4, 9, "2023-02-05"),
(5, 1, "2023-02-06"),
(6, 2, "2023-02-07"),
(7, 3, "2023-02-08"),
(8, 4, "2023-02-09"),
(9, 5, "2023-02-10"),
(10, 6, "2023-02-11"),
(1, 7, "2023-02-12"),
(2, 8, "2023-02-13"),
(3, 9, "2023-02-14"),
(4, 1, "2023-02-15"),
(5, 2, "2023-02-16"),
(6, 3, "2023-02-17"),
(7, 4, "2023-02-18"),
(8, 5, "2023-02-19"),
(9, 6, "2023-02-20"),
(10, 7, "2023-02-21"),
(1, 8, "2023-02-22"),
(2, 9, "2023-02-23"),
(3, 1, "2023-02-24"),
(4, 2, "2023-02-25"),
(5, 3, "2023-02-26"),
(6, 4, "2023-02-27"),
(7, 5, "2023-02-28"),
(8, 6, "2023-03-01"),
(9, 7, "2023-03-02"),
(10, 8, "2023-03-03"),
(1, 9, "2023-03-04"),
(2, 1, "2023-03-05"),
(3, 2, "2023-03-06"),
(4, 3, "2023-03-07"),
(5, 4, "2023-03-08"),
(6, 5, "2023-03-09"),
(7, 6, "2023-03-10"),
(8, 7, "2023-03-11"),
(9, 8, "2023-03-12"),
(10, 9, "2023-03-13");

-- Insert data into the reserve table
INSERT INTO reserve (customer_id, dvd_id) VALUES
(1, 1),
(2, 2),
(4, 3),
(4, 4),
(5, 5),
(5, 6),
(7, 7),
(8, 8),
(10, 9),
(10, 10);

-- Insert data into the rental table
INSERT INTO rental (customer_id, dvd_id, rental_date, due_date) VALUES
(1, 1, '2023-01-01', '2023-01-08'),
(2, 2, '2023-01-02', '2023-01-09'),
(3, 3, '2023-01-03', '2023-01-10'),
(4, 4, '2023-01-04', '2023-01-11'),
(5, 5, '2023-01-05', '2023-01-12'),
(6, 6, '2023-01-06', '2023-01-13'),
(7, 7, '2023-01-07', '2023-01-14'),
(8, 8, '2023-01-08', '2023-01-15'),
(9, 9, '2023-01-09', '2023-01-16'),
(10, 10, '2023-01-10', '2023-01-17');

-- Insert data into the payment table
INSERT INTO payment (rental_id, payment_date, amount) VALUES
(1, '2023-01-08', 16),
(2, '2023-01-09', 18),
(3, '2023-01-10', 20),
(4, '2023-01-11', 22),
(5, '2023-01-12', 24),
(6, '2023-01-13', 26),
(7, '2023-01-14', 28),
(8, '2023-01-15', 30),
(9, '2023-01-16', 32),
(10, '2023-01-17', 34);

-- Insert data into the actor table
INSERT INTO actor (first_name, last_name) VALUES
('Keanu', 'Reeves'),
('Leonardo', 'DiCaprio'),
('Morgan', 'Freeman'),
('John', 'Travolta'),
('Heath', 'Ledger'),
('Brad', 'Pitt'),
('Tom', 'Hanks'),
('Marlon', 'Brando'),
('Robert', 'De Niro'),
('Liam', 'Neeson');

-- Insert data into the plays table
INSERT INTO plays (film_id, actor_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- Insert data into the category table
INSERT INTO category (category_name) VALUES
('Action'),
('Thriller'),
('Drama'),
('Crime'),
('Comedy'),
('Romance'),
('Adventure'),
('Horror'),
('Fantasy'),
('Science Fiction');

-- Insert data into the language table
INSERT INTO language (language_name) VALUES
('English'),
('Spanish'),
('French'),
('German'),
('Japanese'),
('Mandarin'),
('Korean'),
('Italian'),
('Russian'),
('Arabic');

-- Insert data into the film_category table
INSERT INTO film_category (film_id, category_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 1),
(6, 2),
(7, 3),
(8, 4),
(9, 1),
(10, 2);, '2023-01-09', 18),
(3, '2023-01-10', 20),
(4, '2023-01-11', 22),
(5, '2023-01-12', 24),
(6, '2023-01-13', 26),
(7, '2023-01-14', 28),
(8, '2023-01-15', 30),
(9, '2023-01-16', 32),
(10, '2023-01-17', 34);

-- Insert data into the film_language table
INSERT INTO film_language (film_id, language_id) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(10, 1);
