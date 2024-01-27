SELECT u.user_id, u.first_name, u.last_name, u.username, u.email
FROM user u
JOIN rental r ON u.user_id = r.customer_id
JOIN dvd d ON r.dvd_id = d.dvd_id
JOIN shop s ON d.shop_id = s.shop_id
WHERE s.manager_id = 3;