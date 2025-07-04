{{
  config(
    materialized = 'incremental',
    database = 'alert-system-464222',
    schema = 'staging',
    alias = 'staging_ecommerce_data',
    partition_by = {
      "field": "event_timestamp",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by = ["customer_id", "event_type"],
    incremental_strategy = "merge",
    unique_key = "event_id"
  )
}}

WITH SOURCE_TABLE AS (
    SELECT *
    FROM {{ source("raw_ecommerce_data", "ecommerce_clickstream") }}
),

events AS (
  SELECT
    {{
        dbt_utils.generate_surrogate_key([
            'UserID',
            'SessionID',
            'Timestamp',
            'EventType'
        ])
    }} AS event_id,
    Timestamp AS event_timestamp,
    SAFE_CAST(UserID AS INT) AS customer_id,
    SAFE_CAST(ProductID AS STRING) AS product_id,
    SAFE_CAST(SessionID AS INT) AS session_id,
    TRIM(LOWER(EventType)) AS event_type,
    SAFE_CAST(Amount AS FLOAT64) AS amount,
    Outcome AS outcome,
    CURRENT_TIMESTAMP() AS _dbt_loaded_at
  FROM SOURCE_TABLE
),


unique_events AS (
  SELECT
    *,
    ROW_NUMBER() OVER(
      PARTITION BY event_id
      ORDER BY event_timestamp ASC
    ) AS row_num
  FROM
    events
)

SELECT *
FROM unique_events
WHERE row_num = 1