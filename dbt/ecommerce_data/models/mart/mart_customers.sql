-- customer anaytics, customer id, total records, total sessions, first_purchase_date, purchase_count, total_revenue
{{
    config(
        partition_by = {
            "field": " first_session",
            "data_type": "timestamp",
            "granularity": "day"
        },
    )
}}

SELECT 
  customer_id,
  COUNT(*) AS customer_events,
  COUNT(DISTINCT session_id) AS total_sessions,
  MIN(DATE_TRUNC(event_timestamp, DAY)) AS first_session,
  MAX(DATE_TRUNC(event_timestamp, DAY)) AS latest_session,
  ROUND(COALESCE(SUM(amount), 0), 2) AS total_revenue,
FROM {{ ref("staging_ecommerce_data") }}
GROUP BY customer_id

