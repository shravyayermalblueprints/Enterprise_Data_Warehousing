with source as (
    select * from {{ source('internal_db', 'orders') }}
),

renamed as (
    select
        id as order_id,
        user_id,
        status,
        cast(order_date as timestamp) as order_placed_at,
        cast(amount as numeric) as order_amount
    from source
)

select * from renamed
