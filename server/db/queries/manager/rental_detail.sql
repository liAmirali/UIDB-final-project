SELECT
    f.title AS film_title,
    COUNT(r.rental_id) AS number_of_rents,
    AVG(f.rate) AS average_score,
    COUNT(d.dvd_id) AS number_of_dvds,
    SUM(CASE WHEN r.return_date > r.due_date THEN 1 ELSE 0 END) AS number_of_delays
FROM
    film f
LEFT JOIN
    dvd d ON f.film_id = d.film_id
LEFT JOIN
    rental r ON d.dvd_id = r.dvd_id
WHERE
    f.film_id = 1;