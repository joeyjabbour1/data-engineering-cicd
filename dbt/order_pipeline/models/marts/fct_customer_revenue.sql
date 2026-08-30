{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
    where is_valid_amount = true
),

customer_revenue as (
    select
        customer_id,
        count(*)        as order_count,
        sum(amount)     as total_revenue,
        avg(amount)     as avg_order_value
    from orders
    group by customer_id
)

select * from customer_revenue