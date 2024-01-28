SELECT
    s.shop_id,
    s.shop_name,
    u.user_id AS manager_id,
    u.first_name AS manager_first_name,
    u.last_name AS manager_last_name,
    a.address,
    a.address2,
    a.district,
    a.postal_code,
    a.phone,
    a.location,
    a.city,
    a.country
FROM
    shop s
JOIN
    user u ON s.manager_id = u.user_id
JOIN
    address a ON s.address_id = a.address_id
WHERE
    s.manager_id = 6;