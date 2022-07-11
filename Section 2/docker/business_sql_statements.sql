-- list of all our customers and their total spending  (assuming date between 1st july to 17th july)
SELECT customer_name, total_spending FROM
(Select customer_id, customer_name, sum(price) as total_spending
FROM transactions
WHERE (date_time BETWEEN '2022-07-01 00:00:00.000000' AND '2022-07-17 00:00:00.000000')
GROUP BY customer_id, customer_name) temp ;


--  top 3 car manufacturers that customers bought by sales (quantity) and the sales number for it in the current month.
With sales_quantity as(
    SELECT manufacturer_id, count(manufacturer_id) as total_sales_quantity
    FROM transactions
    WHERE extract(MONTH FROM date_time) = extract(MONTH FROM now())
)

SELECT manufacturer_name, total_sales_quantity 
FROM (
    SELECT manufacturer_id, total_sales_quantity 
    FROM sales_quantity s
    LEFT JOIN manufacturers m
    on m.manufacturer_id = s.manufacturer_id
)
order by total_sales_quantity desc
limit 3 ;