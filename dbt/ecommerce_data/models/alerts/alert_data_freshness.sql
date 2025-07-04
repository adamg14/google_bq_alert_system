{{
    config(
        materialize = 'view',
        database = 'alert-system-464222',
        schema = 'alerts'
    )
}}

SELECT
  MAX(_dbt_loaded_at) AS latest_data_load,
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(_dbt_loaded_at), HOUR) AS last_updated,
  CASE
    WHEN TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(_dbt_loaded_at), HOUR) > 2 THEN 'WARNING. THERE HAS BEEN NO ACTIVITY FOR THE PAST 2 HOURS.'
    ELSE NULL
  END AS freshness
FROM {{ ref("staging_ecommerce_data") }}