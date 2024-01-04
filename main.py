import json
import logging
import os
import subprocess
import time
from dataclasses import dataclass
from threading import Thread

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    format="%(asctime)s | %(levelname)s: %(message)s", level=logging.INFO
)
"""
ENVIRONMENT VARIABLES:

-> ENVIRONMENT: Environment to be used. Allowed values: dev, qa, staging, prod
-> TARGET: If you want to connect to MySQL (rds) or DocumentDB (mongodb). Allowed values: rds, documentdb.
"""

region = "us-west-2"
local_port = "3000"


@dataclass
class DocumentDbSecret:
    username: str
    password: str


@dataclass
class RdsSecret:
    host: str
    username: str
    password: str
    port: int


def assert_environment_variables():
    environment_variables = {
        "ENVIRONMENT": ["dev", "qa", "staging", "prod"],
        "TARGET": ["rds", "documentdb"],
    }

    for (
        environment_variable_name,
        environment_variable_allowed_values,
    ) in environment_variables.items():
        assert (
            os.getenv(environment_variable_name) in environment_variable_allowed_values
        ), f"Please set environment variable named '{environment_variable_name}' to be one of the following values: {', '.join(environment_variable_allowed_values)}"


def get_secret(secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    secret = get_secret_value_response["SecretString"]
    secret = json.loads(secret)

    return secret


def get_documentdb_secret() -> DocumentDbSecret:
    environment = os.getenv("ENVIRONMENT").title()
    secret_name = f"opos{environment}DocDB-secret"

    secret = get_secret(secret_name)

    return DocumentDbSecret(username=secret["username"], password=secret["password"])


def get_rds_secret() -> RdsSecret:
    environment = os.getenv("ENVIRONMENT").title()
    secret_name = f"Opos{environment}-db-secret"

    secret = get_secret(secret_name)

    return RdsSecret(
        host=secret["host"],
        username=secret["username"],
        password=secret["password"],
        port=secret["port"],
    )


def has_valid_aws_credentials() -> bool:
    sts = boto3.client("sts")
    try:
        response = sts.get_caller_identity()
        logger.info(
            f"Executing script using the following IAM Pricipal: {response['Arn']}"
        )
        return True
    except Exception:
        return False


def get_bastion_host_id() -> str:
    logger.info("Getting bastion host...")
    ec2 = boto3.client("ec2", region_name=region)

    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Name", "Values": [f"{os.getenv('ENVIRONMENT')}-bastion"]}
        ]
    )
    instance_id = response["Reservations"][0]["Instances"][0]["InstanceId"]

    return instance_id


def get_documentdb_endpoint() -> str:
    logger.info("Getting the Endpoint of the DocumentDB Cluster...")

    documentdb = boto3.client("docdb", region_name=region)
    response = documentdb.describe_db_clusters()
    clusters = [
        {"arn": cluster["DBClusterArn"], "endpoint": cluster["Endpoint"]}
        for cluster in response["DBClusters"]
    ]

    endpoint = ""
    for cluster in clusters:
        response = documentdb.list_tags_for_resource(ResourceName=cluster["arn"])
        for tags in response["TagList"]:
            if tags["Key"] == "Environment" and tags["Value"] == os.getenv(
                "ENVIRONMENT"
            ):
                endpoint = cluster["endpoint"]
                break

    if not endpoint:
        raise Exception(
            "It was not possible to find the Endpoint of the DocumentDB cluster... Please debug the code."
        )

    return endpoint

def port_forward(bastion_id: str, endpoint: str, remote_port: str, local_port: str):
    logger.info("Port-forwarding the Bastion Host...")
    parameters = {
        "host": [endpoint],
        "portNumber": [remote_port],
        "localPortNumber": [local_port],
    }
    command = [
        "aws",
        "--region",
        "us-west-2",
        "ssm",
        "start-session",
        "--target",
        bastion_id,
        "--document-name",
        "AWS-StartPortForwardingSessionToRemoteHost",
        "--parameters",
        f"{json.dumps(parameters)}",
    ]
    logger.info(" ".join(command))
    subprocess.call(command)


def connect_mongodb(username: str, password: str, local_port: str):
    logger.info("Connecting to MongoDB database...")
    subprocess.call(["bash", "connect-documentdb.sh", local_port, username, password])


def connect_rds(username: str, password: str, local_port: str):
    logger.info("Connecting to RDS database...")
    subprocess.call(["bash", "connect-rds.sh", local_port, username, password])


if __name__ == "__main__":
    assert_environment_variables()
    if not has_valid_aws_credentials():
        raise Exception(
            "AWS credentials were not found or are invalid! Please set environment variables for to allow AWS connection!"
        )

    bastion_id = get_bastion_host_id()
    if os.getenv("TARGET") == "documentdb":
        documentdb_endpoint = get_documentdb_endpoint()
        secrets = get_documentdb_secret()
        thread = Thread(
            target=port_forward,
            args=[bastion_id, documentdb_endpoint, "27017", local_port],
        )
        thread.start()
        time.sleep(5)
        connect_mongodb(secrets.username, secrets.password, local_port)
    else:
        secrets = get_rds_secret()
        thread = Thread(
            target=port_forward,
            args=[bastion_id, secrets.host, str(secrets.port), local_port],
        )
        thread.start()
        time.sleep(5)
        connect_rds(secrets.username, secrets.password, local_port)
