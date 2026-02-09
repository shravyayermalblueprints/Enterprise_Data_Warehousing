{{
  config(
    materialized = 'table',
    partition_by = {
      "field": "order_placed_at",
      "data_type": "timestamp",
      "granularity": "day"
    },
    cluster_by = ["user_id", "status"]
  )
}}

with orders as (
    select * from {{ ref('stg_orders') }}
)

select
    order_id,
    user_id,
    status,
    order_placed_at,
    order_amount,
    CURRENT_TIMESTAMP() as loaded_at
from orders
