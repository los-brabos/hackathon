import json

# airflow operators
from airflow.utils.dates import days_ago
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from notify import MSTeamsWebhookHook

role_arn = "arn:aws:iam::527612575494:role/VpcxMWAACustomRole"
# role_arn = 'arn:aws:iam::527612575494:role/VPCx-CustomRole-Glue'
artifactory_image = "527612575494.dkr.ecr.us-east-1.amazonaws.com/{{cookiecutter.project_slug}}"

args = {
    'owner': 'airflow',
}

def task_failure_alert(context):
    dag_id = context['dag_run'].dag_id
    
    teams_hook = MSTeamsWebhookHook(
    http_conn_id="jia_ms_teams",
    message=f"Airflow {dag_id} dag FAILED!",
    subtitle="For more info, go to airflow page and check the logs",
    theme_color="FF0000",
    )
    teams_hook.execute()

def processing():
    import boto3
    import json
    from sagemaker.processing import Processor, ProcessingInput, ProcessingOutput
    from sagemaker.network import NetworkConfig
    from datetime import datetime

    network = NetworkConfig(
        enable_network_isolation=False,
        security_group_ids=[
            'sg-0b1274d6966025b1c',
            'sg-02140314d64cfdd7c',
            'sg-0471677711f4c1394',
        ],
        subnets=[
            'subnet-098c9b6a145b9875f'
            ]
    )
    sm = boto3.client('secretsmanager')
    secret_json_as_string = sm.get_secret_value(SecretId='REDSHIFT_LATAM_PROD_ADMIN_PASS')['SecretString']
    
    dl_usr = 'latam_prd_admin'
    db_pwd = json.loads(secret_json_as_string)['latam_prd_admin_pass']
    dl_adr = 'itx-ags-prd-rs-cl-01.cku868xglwj7.us-east-1.redshift.amazonaws.com:5439'
    
    denodo_usr = sm.get_secret_value(SecretId='SERVICE_ACCOUNT_USERNAME')['SecretString']
    denodo_pwd = sm.get_secret_value(SecretId='SERVICE_ACCOUNT_PASSWORD')['SecretString']
    denodo_adr = "jia-datacatalog-prd.jnj.com:9996"
    
    env_dict = {
        "TODAY_DATE": datetime.today().strftime("%Y%m%d"),
        "DL_USR": dl_usr,
        "DL_PWD": db_pwd,
        "DL_ADR": dl_adr,

        "DENODO_USR": denodo_usr,
        "DENODO_ADR": denodo_adr,
        "DENODO_PWD": denodo_pwd,

        "MLFLOW_TRACKING_INSECURE_TLS": "true"
    }

    processor = Processor(
        image_uri=artifactory_image,
        role=role_arn,  # identity['Arn'],
        instance_count=1,
        instance_type="ml.m5.xlarge",
        network_config=network,
        env=env_dict
    )

    processor.run()

dag = DAG(
    dag_id="{{cookiecutter.project_slug}}",
    start_date=datetime(2022, 6, 27),
    default_args=args,
    schedule_interval="@weekly",
    on_failure_callback=task_failure_alert,
    concurrency=1,
    max_active_runs=1,
    user_defined_filters={'tojson': lambda s: json.JSONEncoder().encode(s)}
)


# dummy operator
init_task = DummyOperator(
    task_id='Start',
    dag=dag
)

end_task = DummyOperator(
    task_id='End',
    dag=dag
)


process_task = PythonOperator(
    task_id='SageMaker_Processing_Job',
    python_callable=processing,
    dag=dag
)

init_task >> process_task >> end_task