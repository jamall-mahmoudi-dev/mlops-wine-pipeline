import kfp
from kfp import dsl
from kfp.components import load_component_from_file
from kubernetes.client.models import V1EnvVar
from kfp.onprem import use_k8s_secret
import os

# Load components
web_downloader_op = load_component_from_file('components/download/component.yaml')
preprocess_op = load_component_from_file('components/preprocess/component.yaml')
training_op = load_component_from_file('components/train/component.yaml')
deploy_op = load_component_from_file('components/deploy/component.yaml')

@dsl.pipeline(
    name="wine_quality_pipeline",
    description="End-to-end wine quality prediction pipeline"
)
def wine_pipeline(url: str):
    download_task = web_downloader_op(url=url)
    preprocess_task = preprocess_op(file_path=download_task.outputs['data'])
    
    train_task = training_op(file_path=preprocess_task.outputs['output']) \
        .add_env_variable(V1EnvVar(name='MLFLOW_TRACKING_URI', value='http://mlflow-server.kubeflow.svc.cluster.local:5000')) \
        .add_env_variable(V1EnvVar(name='MLFLOW_S3_ENDPOINT_URL', value='http://minio.kubeflow.svc.cluster.local:9000')) \
        .apply(use_k8s_secret(secret_name='mlpipeline-minio-artifact',
                              k8s_secret_key_to_env={'accesskey': 'AWS_ACCESS_KEY_ID', 'secretkey': 'AWS_SECRET_ACCESS_KEY'}))
    
    deploy_task = deploy_op(model_uri=train_task.output)
