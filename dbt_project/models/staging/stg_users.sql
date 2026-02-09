with source as (
    select * from {{ source('internal_db', 'users') }}
),

renamed as (
    select
        id as user_id,
        email,
        first_name,
        last_name,
        cast(created_at as timestamp) as created_at,
        cast(updated_at as timestamp) as updated_at
    from source
)

select * from renamed
