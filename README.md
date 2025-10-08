# MLOps Wine Quality Pipeline

This project demonstrates an end-to-end MLOps pipeline using Kubeflow Pipelines, MLFlow, Minio, and Seldon Core. 
It downloads a wine dataset, preprocesses it, trains an ElasticNet model, and deploys it as a microservice.

## Requirements
- Kubeflow Pipelines
- Minio
- MLFlow
- Kubernetes cluster with Seldon Core

## Running
1. Install dependencies: `pip install -r requirements.txt`
2. Run the pipeline: `python pipeline.py`
3. Upload generated YAML to Kubeflow dashboard and execute
