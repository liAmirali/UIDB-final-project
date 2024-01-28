SELECT
    r.reserve_id,
    r.customer_id,
    r.dvd_id,
    r.created_at
FROM
    reserve r
JOIN
    dvd d ON r.dvd_id = d.dvd_id
JOIN
    shop s ON d.shop_id = s.shop_id
WHERE
    s.manager_id = 3
    AND r.accepted is NULL;