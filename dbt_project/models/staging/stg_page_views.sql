with source as (
    select * from {{ source('event_logs', 'page_views') }}
),

renamed as (
    select
        event_id,
        user_id,
        session_id,
        page_url,
        cast(event_timestamp as timestamp) as viewed_at,
        device_type
    from source
)

select * from renamed
