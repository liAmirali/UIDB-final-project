SELECT
    f.title AS film_title,
    f.description,
    f.release_date,
    f.rate,
    f.rent_cost_per_day,
    f.penalty_cost_per_day
FROM
    film f
JOIN
    dvd d ON f.film_id = d.film_id
JOIN
    shop s ON d.shop_id = s.shop_id
WHERE
    s.manager_id = 3
ORDER BY
    f.rate DESC
