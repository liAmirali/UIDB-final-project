SELECT
    r.rental_id,
    r.customer_id,
    r.dvd_id,
    r.rental_date,
    r.due_date
FROM
    rental r
JOIN
    dvd d ON r.dvd_id = d.dvd_id
JOIN
    shop s ON d.shop_id = s.shop_id
WHERE
    s.manager_id = 1
    AND r.return_date IS NULL;
