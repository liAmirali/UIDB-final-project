SELECT
    p.payment_id,
    p.rental_id,
    p.payment_date,
    p.amount,
    r.customer_id,
    r.dvd_id,
    r.rental_date,
    r.due_date,
    r.return_date,
    r.status,
    r.rate,
    r.last_update,
    s.shop_id,
    s.shop_name,
    s.manager_id
FROM
    payment p
JOIN
    rental r ON p.rental_id = r.rental_id
JOIN
    dvd d ON r.dvd_id = d.dvd_id
JOIN
    shop s ON d.shop_id = s.shop_id
WHERE
    s.manager_id = 6 AND r.customer_id = 2