with users as (
    select * from {{ ref('dim_users') }}
),

orders as (
    select * from {{ ref('fact_orders') }}
),

user_orders as (
    select
        user_id,
        count(order_id) as total_orders,
        sum(order_amount) as total_spent,
        min(order_placed_at) as first_order_date,
        max(order_placed_at) as last_order_date
    from orders
    group by 1
),

final as (
    select
        u.user_id,
        u.first_name,
        u.last_name,
        u.email,
        coalesce(uo.total_orders, 0) as total_orders,
        coalesce(uo.total_spent, 0) as total_spent,
        uo.first_order_date,
        uo.last_order_date
    from users u
    left join user_orders uo on u.user_id = uo.user_id
)

select * from final
