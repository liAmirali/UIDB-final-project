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
    film_category fc ON f.film_id = fc.film_id
JOIN
    category c ON fc.category_id = c.category_id
JOIN
    film_language fl ON f.film_id = fl.film_id
JOIN
    language l ON fl.language_id = l.language_id
JOIN
    dvd d ON f.film_id = d.film_id
JOIN
    shop s ON d.shop_id = s.shop_id
WHERE
    s.manager_id = 3
    AND c.category_name = 'Action'
ORDER BY
    f.rate DESC
LIMIT 1;
