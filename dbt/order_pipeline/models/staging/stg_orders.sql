with source as (
    select * from {{ source('raw', 'orders') }}
),

cleaned as (
    select
        cast(order_id as integer)         as order_id,
        trim(customer_id)                 as customer_id,
        cast(amount as decimal(12,2))     as amount,
        case
            when cast(amount as decimal(12,2)) > 0 then true
            else false
        end                               as is_valid_amount,
        batch_id,
        source_file,
        ingestion_timestamp
    from source
)

select * from cleaned