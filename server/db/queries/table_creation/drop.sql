SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `address`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `film`;
DROP TABLE IF EXISTS `shop`;
DROP TABLE IF EXISTS `dvd`;
DROP TABLE IF EXISTS `reserve`;
DROP TABLE IF EXISTS `rental`;
DROP TABLE IF EXISTS `payment`;
DROP TABLE IF EXISTS `actor`;
DROP TABLE IF EXISTS `plays`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `language`;
DROP TABLE IF EXISTS `film_category`;
DROP TABLE IF EXISTS `film_language`;
DROP TRIGGER IF EXISTS `on_before_rent_insert`;
DROP TRIGGER IF EXISTS `check_manager_limit`;
DROP TRIGGER IF EXISTS `check_rent_count_limit`;
DROP TRIGGER IF EXISTS `check_rental_duration`;
SET FOREIGN_KEY_CHECKS = 1;
