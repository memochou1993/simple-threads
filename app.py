import os

import aws_cdk
from dotenv import load_dotenv

from deployment.simple_threads_stack import SimpleThreadsStack

load_dotenv()

app = aws_cdk.App()

env = aws_cdk.Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION"),
)

SimpleThreadsStack(
    app,
    "SimpleThreadsStack",
    env=env,
)

app.synth()
