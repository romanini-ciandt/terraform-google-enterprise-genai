from datetime import datetime
from google.cloud import aiplatform
import os
# from pathlib import Path as path
# from urllib.parse import urlparse
# import os
# from six.moves import urllib
# import tempfile
# import numpy as np
# import pandas as pd
# import tensorflow as tf
# import tensorflow_hub as hub
# from google.cloud import aiplatform
# from google.cloud import bigquery
# from google.api_core.exceptions import GoogleAPIError
# from typing import NamedTuple

class vertex_ai_pipeline:
    def __init__(self, 
        PROJECT_ID:str = "feisty-outlet-408722", \
        PROD_PROJECT_ID:str = 'prod-408722', \
        REGION:str = "us-central1", \
        BUCKET_URI:str = "gs://vertexpipe_staging", \
        DATA_PATH:str = "data", \
        KFP_COMPONENTS_PATH:str = "components", \
        SRC:str = "src", \
        BUILD:str = "build", \
        TRAINING_FILE:str = 'adult.data.csv', \
        EVAL_FILE:str = 'adult.test.csv', \
        DATASET_ID:str = 'census_dataset', \
        TRAINING_TABLE_ID:str = 'census_train_table', \
        EVAL_TABLE_ID:str = 'census_eval_table', \
        RUNNER:str = "DataflowRunner", \
        JOB_NAME:str = "census-ingest", \
        SERVICE_ACCOUNT:str = "578182842955-compute@developer.gserviceaccount.com"
        ):

        self.timestamp = datetime.now().strftime("%d_%H_%M_%S")
        self.PROJECT_ID = PROJECT_ID
        self.PROD_PROJECT_ID = PROD_PROJECT_ID
        self.REGION = REGION 
        self.BUCKET_URI = BUCKET_URI
        self.DATA_PATH = DATA_PATH

        DAGS_FOLDER = os.environ.get("DAGS_FOLDER", "/")
        COMMON_FOLDER = os.path.join(DAGS_FOLDER, "common")
        self.yaml_file_path = os.path.join(COMMON_FOLDER, "vertex-ai-pipeline/pipeline_package.yaml")

        self.KFP_COMPONENTS_PATH = KFP_COMPONENTS_PATH
        self.SRC = SRC
        self.BUILD = BUILD
        self.Image = f"{REGION}-docker.pkg.dev/{PROJECT_ID}/pipelinerepo/pipeline_tutorial:latest"

        self.DATA_URL = f'{self.BUCKET_URI}/data'
        self.TRAINING_FILE = 'adult.data.csv'
        self.EVAL_FILE = 'adult.test.csv'
        self.TRAINING_URL = '%s/%s' % (self.DATA_URL, self.TRAINING_FILE)
        self.EVAL_URL = '%s/%s' % (self.DATA_URL, self.EVAL_FILE)
        self.DATASET_ID = 'census_dataset'
        self.TRAINING_TABLE_ID = 'census_train_table'
        self.EVAL_TABLE_ID = 'census_eval_table'
        self.RUNNER = "DataflowRunner"
        self.JOB_NAME="census-ingest"
        self.SERVICE_ACCOUNT = SERVICE_ACCOUNT

        self.create_bq_dataset_query = f"""
        CREATE SCHEMA IF NOT EXISTS {self.DATASET_ID}
        """

        self.data_config={
         "train_data_url": self.TRAINING_URL,
         "eval_data_url": self.EVAL_URL,
         "bq_dataset": self.DATASET_ID,
         "bq_train_table": TRAINING_TABLE_ID,
         "bq_eval_table": EVAL_TABLE_ID,
        }

        self.dataflow_config={
                        "job_name": JOB_NAME,
                        "requirements_file_path": f'{BUCKET_URI}/requirements.txt',
                        "python_file_path": f'{BUCKET_URI}/src/ingest_pipeline.py',
                        "setup_file_uri": f'{BUCKET_URI}/setup.py',
                        "temp_location": f'{BUCKET_URI}/temp_dataflow',
                        "runner": RUNNER,
        }
        self.train_config={
                     'lr': 0.01, 
                     'epochs': 5, 
                     'base_train_dir': f'{BUCKET_URI}/training', 
                     'tb_log_dir': f'{BUCKET_URI}/tblogs',
        }

        self.deployment_config={
            'image': "us-docker.pkg.dev/cloud-aiplatform/prediction/tf2-cpu.2-8:latest",
            'model_name': "income_bracket_predictor_prod",
            'endpoint_name': "census_income_endpoint_prod",
            'min_nodes': 2,
            'max_nodes': 4,
            'deployment_project': self.PROD_PROJECT_ID,
            "encryption": '',
            "service_account": self.SERVICE_ACCOUNT,
        }

        self.monitoring_config={
            'email': 'majid.alikhani@badal.io', 
            'name': 'census_monitoring'  
        }

        self.pipelineroot = f'{BUCKET_URI}/pipelineroot'

    def execute(self):
        pipeline = aiplatform.PipelineJob(
            display_name=f"census_income_{self.timestamp}",
            template_path=self.yaml_file_path,
            pipeline_root=self.pipelineroot,
            parameter_values={
                "create_bq_dataset_query": self.create_bq_dataset_query,
                "bq_dataset": self.data_config['bq_dataset'],
                "bq_train_table": self.data_config['bq_train_table'],
                "bq_eval_table": self.data_config['bq_eval_table'],
                "job_name": self.dataflow_config['job_name'],
                "train_data_url": self.data_config['train_data_url'],
                "eval_data_url": self.data_config['eval_data_url'],
                "requirements_file_path": self.dataflow_config['requirements_file_path'],
                "python_file_path": self.dataflow_config['python_file_path'],
                "dataflow_temp_location": self.dataflow_config['temp_location'],
                "runner": self.dataflow_config['runner'],
                "project": self.PROJECT_ID,
                "region": self.REGION,
                "model_dir": f"{self.BUCKET_URI}",
                "bucket_name": self.BUCKET_URI[5:],
                "epochs": self.train_config['epochs'],
                "lr": self.train_config['lr'],
                "base_train_dir": self.train_config['base_train_dir'],
                "tb_log_dir": self.train_config['tb_log_dir'],
                "deployment_image": self.deployment_config['image'],
                "deployed_model_name": self.deployment_config["model_name"],
                "endpoint_name": self.deployment_config["endpoint_name"],
                "min_nodes": self.deployment_config["min_nodes"],
                "max_nodes": self.deployment_config["max_nodes"],
                "deployment_project": self.deployment_config["deployment_project"]
                "encryption": self.deployment_config.get("encryption"),
                "service_account": self.deployment_config["service_account"],
                "monitoring_name": self.monitoring_config['name'],
                "monitoring_email": self.monitoring_config['email'],

            },
            enable_caching=False,
        )
        
        return pipeline.run(service_account=self.SERVICE_ACCOUNT)