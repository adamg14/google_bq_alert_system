{{
  config(
    materialized = 'incremental',
    database = 'alert-system-464222',
    schema = 'staging',
    alias = 'staging_ecommerce_data',
    tags = ['staging', 'ecommerce'],
    
    partition_by = {
      "field": "event_timestamp",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by = ["customer_id", "event_type"],
    incremental_strategy = "merge"
  )
}}

WITH SOURCE_TABLE AS (
    SELECT *
    FROM {{ source("raw_ecommerce_data", "ecommerce_clickstream") }}

    {% if is_incremental() %}
        WHERE _loaded_at > (SELECT MAX(_loaded_at) FROM {{ this }})
     {% endif %}
)

SELECT
    {{
        dbt_utils.generate_surrogate_key([
            'UserID',
            'SessionID',
            'Timestamp'
        ])
    }} AS event_id,
    Timestamp AS event_timestamp,
    SAFE_CAST(UserID AS INT) AS customer_id,
    SAFE_CAST(ProductID AS INT) AS product_id,
    SAFE_CAST(SessionID AS INT) AS session_id,
    TRIM(LOWER(EventType)) AS event_type,
    SAFE_CAST(Amount AS FLOAT64) AS amount,
    Outcome AS outcome,
    CURRENT_TIMESTAMP() AS _dbt_loaded_at
FROM SOURCE_TABLE
