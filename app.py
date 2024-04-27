import os

import aws_cdk
from dotenv import load_dotenv

from deployment.cdk_python_example_stack import CdkPythonExampleStack

load_dotenv()

app = aws_cdk.App()

env = aws_cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION"),
)

CdkPythonExampleStack(
    app,
    "CdkPythonExampleStack",
    env=env,
)

app.synth()
