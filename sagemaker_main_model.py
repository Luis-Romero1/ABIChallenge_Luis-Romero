import boto3
import sagemaker
from sagemaker.estimator import Estimator
import os

# Configurar el cliente de SageMaker
boto_session = boto3.Session(region_name=os.getenv('AWS_REGION'))
sagemaker_session = sagemaker.Session(boto_session=boto_session)
role = os.getenv("ROLL_IAM")

# Configurar VPC
vpc_config = {
    'Subnets': [os.getenv("SUBPRI"), os.getenv("SUBDB")],
    'SecurityGroupIds': [os.getenv("SGIN"), os.getenv("SGOUT")]
}

# Obtener la URI de la imagen de ECR
ecr_image = f"{os.getenv('AWS_ECR_LOGIN_URIX')}/{os.getenv('ECR_REPOSITORY_NAME')}:latest"

# Configurar el estimador
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
    }
)

# Entrenar el modelo
estimator.fit()

# Desplegar el modelo
predictor = estimator.deploy(
    initial_instance_count=1,
    instance_type="ml.m4.xlarge",
    endpoint_name="Iris_endpoint"
)

print("Modelo entrenado y desplegado exitosamente.")