{{
  config(
    materialized = 'table',
    partition_by = {'field': 'cohort', 'data_type': 'date'}
  )
}}

WITH customer_cohort AS (
  SELECT
    DATE(DATE_TRUNC(event_timestamp, MONTH)) AS cohort,
    customer_id
  FROM {{ ref("staging_ecommerce_data") }}
  WHERE event_type = 'purchase'
  GROUP BY customer_id, DATE(DATE_TRUNC(event_timestamp, MONTH))
),

customer_cohort_metrics AS (
  SELECT 
    customer.customer_id AS customer_id,
    customer.cohort AS cohort,
    DATE_DIFF(DATE(DATE_TRUNC(metrics.event_timestamp, MONTH)), customer.cohort, MONTH) AS active_months,
    COUNT(DISTINCT session_id) AS total_sessions,
    COALESCE(ROUND(SUM(amount), 2), 0) AS total_revenue,
    COUNT(CASE WHEN metrics.event_type = 'purchase' THEN metrics.session_id END) AS purchase_count
  FROM {{ ref("staging_ecommerce_data") }} metrics
  JOIN customer_cohort customer
  ON metrics.customer_id = customer.customer_id
  GROUP BY customer.customer_id, customer.cohort, DATE_DIFF(DATE(DATE_TRUNC(metrics.event_timestamp, MONTH)), customer.cohort, MONTH)
),

cohort_metrics AS (
  SELECT
    cohort,
    COUNT(DISTINCT customer_id) AS cohort_size,
    active_months,
    COUNT(DISTINCT CASE WHEN purchase_count > 0 THEN customer_id END) AS retained_customers,
    SUM(purchase_count) AS purchase_count,
    SUM(total_revenue) AS total_revenue,
    SAFE_DIVIDE(SUM(total_revenue), COUNT(DISTINCT CASE WHEN purchase_count > 0 THEN customer_id END)) AS aov,
    SUM(total_sessions) AS total_sessions
  FROM customer_cohort_metrics
  WHERE active_months >= 0
  GROUP BY cohort, active_months
)

SELECT
  *,
  SAFE_DIVIDE(retained_customers, cohort_size) AS retention_rate,

FROM cohort_metrics