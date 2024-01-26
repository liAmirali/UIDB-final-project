INSERT INTO address (address, address2, district, postal_code, phone, location, city, country) VALUES
('789 Elm St', NULL, 'Eastside', '13579', '555-2468', 'Everywhere', 'Village', 'USA'),
('101 Pine St', NULL, 'Northside', '24680', '555-3691', 'Nowhere', 'Town', 'USA'),
('321 Maple St', NULL, 'Southside', '97531', '555-8024', 'Anywhere', 'City', 'USA'),
('876 Park St', NULL, 'Central', '98765', '555-1357', 'Nowhere', 'Metropolis', 'USA'),
('543 Cherry St', NULL, 'Downtown', '86420', '555-9876', 'Anywhere', 'Big City', 'USA');


INSERT INTO user (first_name, last_name, username, password, email, address_id, role) VALUES
('Sarah', 'Johnson', 'sarahj', 'password789', 'sarah@example.com', 3, 'customer'),
('Mike', 'Brown', 'mikeb', 'password101', 'mike@example.com', 4, 'customer'),
('Emily', 'Wilson', 'emilyw', 'password321', 'emily@example.com', 1, 'customer'),
('David', 'Jones', 'davidj', 'password456', 'david@example.com', 2, 'manager'),
('Jennifer', 'Davis', 'jenniferd', 'password654', 'jennifer@example.com', 5, 'customer');


INSERT INTO film (title, description, release_date, rate, rent_cost_per_day, penalty_cost_per_day) VALUES
('Inception', 'A mind-bending thriller', '2010-07-16', 5, 3, 4),
('The Shawshank Redemption', 'A drama film', '1994-10-14', 5, 2, 3),
('Forrest Gump', 'A comedy-drama film', '1994-07-06', 4, 2, 3),
('The Dark Knight', 'A superhero film', '2008-07-18', 5, 3, 4),
('The Godfather', 'A crime film', '1972-03-24', 5, 2, 3);

INSERT INTO shop (shop_name, manager_id, address_id) VALUES
('Eastside Shop', 4, 1),
('Northside Shop', 4, 2),
('Southside Shop', 4, 3),
('Central Shop', 4, 4),
('Downtown Shop', 4, 5);

INSERT INTO dvd (film_id, shop_id, production_date) VALUES
(3, 1, '2023-01-15'),
(4, 2, '2023-02-20'),
(1, 3, '2023-03-25'),
(2, 4, '2023-04-05'),
(5, 5, '2023-04-12');

INSERT INTO reserve_req (customer_id, dvd_id, accepted) VALUES
(3, 3, TRUE),
(3, 4, FALSE),
(4, 5, TRUE);

INSERT INTO rental (customer_id, dvd_id, rental_date, due_date, accepted, return_date) VALUES
(3, 3, '2023-03-01', '2023-03-08', TRUE, '2023-03-11'),
(3, 4, '2023-03-05', '2023-03-12', FALSE, NULL),
(4, 5, '2023-04-01', '2023-04-08', TRUE, '2023-03-11'),
(5, 2, '2023-06-15', '2023-06-22', TRUE, '2023-03-13'),
(3, 4, '2023-07-05', '2023-07-12', FALSE, '2023-03-11'),
(4, 3, '2023-07-10', '2023-07-17', TRUE, '2023-03-11'),
(5, 1, '2023-08-01', '2023-08-08', TRUE, '2023-03-15'),
(3, 5, '2023-08-15', '2023-08-22', FALSE, '2023-03-11'),
(4, 2, '2023-09-01', '2023-09-08', TRUE, NULL),
(5, 3, '2023-09-10', '2023-09-17', FALSE, NULL),
(3, 1, '2023-10-05', '2023-10-12', TRUE, '2023-03-11'),
(4, 4, '2023-10-15', '2023-10-22', TRUE, '2023-03-11'),
(5, 5, '2023-11-01', '2023-11-08', FALSE, NULL);

INSERT INTO payment (rental_id, payment_date, amount) VALUES
(2, '2023-03-01', 6),
(2, '2023-03-08', 3),
(3, '2023-04-01', 4);


INSERT INTO actor (first_name, last_name) VALUES
('Leonardo', 'DiCaprio'),
('Tim', 'Robbins'),
('Tom', 'Hanks'),
('Christian', 'Bale'),
('Marlon', 'Brando');

INSERT INTO plays (film_id, actor_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO category (category_name) VALUES
('Thriller'),
('Drama'),
('Comedy'),
('Superhero'),
('Crime');


INSERT INTO language (language_name) VALUES
('English'),
('French'),
('German'),
('Italian'),
('Japanese');


INSERT INTO film_category (film_id, category_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO film_language (film_id, language_id) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 1),
(5, 1);
