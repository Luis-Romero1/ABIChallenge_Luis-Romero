import boto3
import sagemaker
from sagemaker.estimator import Estimator
import os
import time


boto_session = boto3.Session(region_name=os.getenv('AWS_REGION'))
sagemaker_session = sagemaker.Session(boto_session=boto_session)
role = os.getenv("ROLL_IAM")


vpc_config = {
    'Subnets': [os.getenv("SUBPRI"), os.getenv("SUBDB")],
    'SecurityGroupIds': [os.getenv("SGIN"), os.getenv("SGOUT")]
}


ecr_image = f"{os.getenv('AWS_ECR_LOGIN_URIX')}/{os.getenv('ECR_REPOSITORY_NAME')}:latest"


job_name = f"iris-training-{int(time.time())}"

training_image_config = {
    'TrainingRepositoryAccessMode': 'VPC'
}


estimator = Estimator(
    image_uri=ecr_image,
    role=role,
    instance_count=1,
    instance_type="ml.m5.large",
    vpc_config=vpc_config,
    use_spot_instances=True,
    max_wait=7200,
    max_run=3600,
    sagemaker_session=sagemaker_session,
    environment={
        "ACESS_POINT": os.getenv("ACESS_POINT"),
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_USER": os.getenv("DB_USER"),
        "ENV": os.getenv("ENV")
    },training_image_config=training_image_config
)


try:
    estimator.fit(job_name=job_name)
except Exception as e:
    print(f"Error durante el entrenamiento: {str(e)}")
    raise


try:
    predictor = estimator.deploy(
        initial_instance_count=1,
        instance_type="ml.m4.xlarge",
        endpoint_name=f"iris-endpoint-{int(time.time())}"
    )
    print("Modelo entrenado y desplegado exitosamente.")
except Exception as e:
    print(f"Error durante el despliegue: {str(e)}")
    raise
