SELECT * FROM order_table

DESCRIBE order_table;

CREATE OR REPLACE VIEW order_view AS 
	SELECT order_id AS id
        , to_char(order_price, '9,999,999') || '원' AS price
        , order_date AS o_date
        FROM order_table
        
        
SELECT id, price, o_date
FROM order_view
UNION ALL
SELECT 999 AS id, TO_CHAR(SUM(TO_NUMBER(REPLACE(price, '원', ''))), '9,999,999') || '원' AS price, NULL AS o_date
FROM order_view;




SELECT id, price, o_date
FROM (
    SELECT order_id AS id,
           TO_CHAR(order_price, '9,999,999') || '원' AS price,
           order_date AS o_date
    FROM order_table
    UNION ALL
    SELECT 0 AS id,
           TO_CHAR(SUM(order_price), '9,999,999') || '원' AS price,
           NULL AS o_date
    FROM order_table
);


SELECT * FROM order_view 
WHERE o_date BETWEEN '2025-03-22' AND '2025-03-24';