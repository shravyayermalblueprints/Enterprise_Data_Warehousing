with users as (
    select * from {{ ref('stg_users') }}
)

select
    user_id,
    first_name,
    last_name,
    email,
    created_at,
    updated_at
from users
