{{
    config(
        materialize = 'view',
        database = 'alert-system-464222',
        schema = 'alerts'
    )
}}

with day_volume AS (
  SELECT
    DATE_TRUNC(event_timestamp, DAY) AS day,
    COUNT(*) AS daily_volume
  FROM {{ ref("staging_ecommerce_data") }}
  GROUP BY DATE_TRUNC(event_timestamp, DAY)
),

daily_volume_calculations AS (
  SELECT 
    AVG(daily_volume) AS avg_daily_volume,
    STDDEV(daily_volume) AS std_daily_volume
  FROM day_volume
)

SELECT
  day,
  "WARNING. The following days are showing irregular volume" AS volume_alert
FROM day_volume, daily_volume_calculations
WHERE daily_volume > (avg_daily_volume + 3 * std_daily_volume)
OR daily_volume < (avg_daily_volume - 3 * std_daily_volume)

-- REMEMBER TO ADD A TIME CONDITION WHEN QUERYING THE ALERTS TABLE SO THAT PREVIOUS ALERTS ARE NOT SHOWN 