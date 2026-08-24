from datetime import datetime

from airflow import DAG

try:
    from airflow.providers.docker.operators.docker import DockerOperator
except ImportError:  # pragma: no cover
    from airflow.operators.docker import DockerOperator

default_args = {
    "api_version": "auto",
    "auto_remove": True,
    "docker_url": "unix://var/run/docker.sock",
    "network_mode": "bridge",
}

with DAG(
    dag_id="order_pipeline_multitask",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    extract = DockerOperator(
        task_id="extract_orders",
        image="order-pipeline:dev",
        command="python -m order_pipeline extract",
        **default_args,
    )

    validate = DockerOperator(
        task_id="validate_orders",
        image="order-pipeline:dev",
        command="python -m order_pipeline validate",
        **default_args,
    )

    transform = DockerOperator(
        task_id="transform_orders",
        image="order-pipeline:dev",
        command="python -m order_pipeline transform",
        **default_args,
    )

    load = DockerOperator(
        task_id="load_orders",
        image="order-pipeline:dev",
        command="python -m order_pipeline load",
        **default_args,
    )

    extract >> validate >> transform >> load
