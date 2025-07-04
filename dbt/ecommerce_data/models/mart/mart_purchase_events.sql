{{
    config(
        materialize = "incremental",
        partition_by = {
            "field": "event_timestamp",
            "data_type": "timestamp",
            "granularity": "day"
        },
        cluster_by = ["product_id", "customer_id"],
    )
}}

SELECT
    *
FROM {{ ref("staging_ecommerce_data") }}
WHERE event_type = 'purchase'