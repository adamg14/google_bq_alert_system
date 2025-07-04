{{
  config(
    materialized = 'incremental',
    partition_by = {
        'field': 'day',
        'data_type': 'date'
    }
  )
}}

WITH day_stats AS (
  SELECT
    DATE(event_timestamp) AS day,
    COUNT(DISTINCT session_id) AS total_sessions,
    COUNT(CASE WHEN event_type = 'product_view' THEN session_id END) AS total_product_views,
    COUNT(CASE WHEN event_type = 'click' THEN session_id END) AS total_clicks,
    COUNT(CASE WHEN event_type = 'add_to_cart' THEN session_id END) AS total_cart_adds,
    COUNT(CASE WHEN event_type = 'purchase' THEN session_id END) AS total_purchases,
    ROUND(SUM(amount), 2) AS total_revenue,
    COUNT(DISTINCT customer_id) AS total_customers  
  FROM {{ ref("staging_ecommerce_data") }}
  GROUP BY DATE(event_timestamp)
)

SELECT 
  *,
  ROUND(SAFE_DIVIDE(total_clicks, total_product_views), 2) AS ctr,
  ROUND(SAFE_DIVIDE(total_purchases, total_product_views), 2) AS cvr,
  ROUND(SAFE_DIVIDE(total_revenue, total_purchases), 2) AS aov
FROM day_stats