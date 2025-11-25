{{ config(materialized='table') }}

SELECT 
    o.order_date,
    o.order_id,
    SUM(oi.total_price) AS total_price
FROM {{ ref('stg_orders') }} o
LEFT JOIN {{ ref('stg_order_items') }} oi
ON o.order_id = oi.order_id
GROUP BY 1, 2

--^ note
-- SELECT 
--     o.order_date,      -- ← position 1
--     o.order_id,        -- ← position 2
--     SUM(oi.total_price) AS total_price

--^ GROUP BY 1, 2 is equivalent to:

-- GROUP BY o.order_date, o.order_id


