from sagemaker.sklearn.model import SKLearnModel
from sagemaker.sklearn.estimator import SKLearn
import os

FRAMEWORK_VERSION = "0.23-1"


endpoint_name="Iris_endpoint"

rolef = os.getenv("ROLL_IAM")


try:
    vpc_configf = {
        'Subnets': [os.getenv("SUBPRI"), os.getenv("SUBDB")],  # Tus subnets
        'SecurityGroupIds': [os.getenv("SGIN"),os.getenv("SGOUT")]  # Tus security groups
    }
except:
    vpc_configf = {
        'Subnets': ["subnet-0481d2f1cb01b8236", "subnet-064f2feaf0c3d4c0a"],  # Tus subnets
        'SecurityGroupIds': ["sg-0c4847fce2396e1be","sg-0078bd29f6e0aa50c"]  # Tus security groups
    }

training_image_config = {
    'TrainingRepositoryAccessMode': 'VPC'
}
# Definir el estimador y entrenar
sklearn_estimator = SKLearn(
    entry_point="main.py",  # Archivo principal que se ejecutará
    source_dir=".",  # El directorio actual contiene todos los archivos necesarios
    role=rolef,
    instance_count=1,
    instance_type="ml.m5.large",
    framework_version=FRAMEWORK_VERSION,
    base_job_name="Custom-iris-sklearn",
    use_spot_instances=True,
    vpc_config=vpc_configf,
    max_wait=7200,
    max_run=3600,
    dependencies=['requirements.txt'],
    training_image_config=training_image_config  # Asegura la instalación de las dependencias
)
# Entrenamiento del modelo
sklearn_estimator.fit(wait=True)

# Recuperar la ubicación de los artefactos del modelo en S3
model_data = sklearn_estimator.model_data

# Crear un objeto SKLearnModel usando los artefactos del modelo en S3
model = SKLearnModel(
    model_data=model_data,
    role=rolef,
    entry_point="main.py",  # Mismo script que usaste para entrenar
    source_dir=".",  # Directorio actual contiene todos los archivos necesarios
    framework_version=FRAMEWORK_VERSION,
    dependencies=['requirements.txt'],  # Asegura la instalación de las dependencias
    vpc_config=vpc_configf,
    training_image_config=training_image_config  # Opcional, si tienes VPC configurado
)

# Desplegar el modelo como un endpoint
predictor = model.deploy(
    initial_instance_count=1,
    instance_type="ml.m4.xlarge",
    endpoint_name=endpoint_name,
)
