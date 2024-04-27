import os

from aws_cdk import Duration, Size, Stack, aws_apigateway, aws_ec2, aws_iam, aws_lambda, aws_logs
from constructs import Construct


class CdkPythonExampleStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = self.create_vpc()
        self.lambda_function = self.create_lambda_function()
        self.api_gateway = self.create_api_gateway()

    def create_vpc(self):
        vpc = aws_ec2.Vpc.from_lookup(
            self,
            "SelectedVpc",
            vpc_id=os.environ.get("AWS_VPC_ID"),
        )

        return vpc

    def create_lambda_function(self):
        lambda_role = aws_iam.Role(
            self,
            "CdkPythonExampleLambdaRole",
            description="CDK Python Example Lambda Role",
            assumed_by=aws_iam.CompositePrincipal(
                aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )
        lambda_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "CdkPythonExampleAWSLambdaBasicExecutionRolePolicy",
                "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
            )
        )
        lambda_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "CdkPythonExampleAWSLambdaVPCAccessExecutionRolePolicy",
                "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole",
            )
        )

        lambda_function = aws_lambda.Function(
            self,
            "CdkPythonExampleLambdaFunction",
            description="CDK Python Example Lambda Function",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            code=aws_lambda.Code.from_asset("lambda"),
            handler="hello.handler",
            architecture=aws_lambda.Architecture.ARM_64,
            memory_size=512,
            timeout=Duration.seconds(30),
            vpc=self.vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS, one_per_az=True),
            role=lambda_role,
            environment={},
        )

        return lambda_function

    def create_api_gateway(self):
        log_group = aws_logs.LogGroup(
            self,
            "CdkPythonExampleLogGroup",
            retention=aws_logs.RetentionDays.ONE_MONTH,
        )

        api_gateway = aws_apigateway.RestApi(
            self,
            "CdkPythonExampleApiGateway",
            description="CDK Python Example Api Gateway",
            min_compression_size=Size.kibibytes(1),
            endpoint_types=[aws_apigateway.EndpointType.REGIONAL],
            cloud_watch_role=True,
            deploy_options=aws_apigateway.StageOptions(
                stage_name="production",
                metrics_enabled=True,
                access_log_destination=aws_apigateway.LogGroupLogDestination(log_group),
            ),
        )

        usage_plan = api_gateway.add_usage_plan(
            "CdkPythonExampleUsagePlan",
            description="CDK Python Example Usage Plan",
            throttle=aws_apigateway.ThrottleSettings(
                burst_limit=50,
                rate_limit=100,
            ),
        )

        api_key = aws_apigateway.ApiKey(
            self,
            "CdkPythonExampleApiKey",
            description="CDK Python Example Api Key",
        )

        usage_plan.add_api_key(api_key)

        v1_resource = api_gateway.root.add_resource("v1")
        v1_resource.add_cors_preflight(
            allow_origins=aws_apigateway.Cors.ALL_ORIGINS,
            allow_methods=aws_apigateway.Cors.ALL_METHODS,
            max_age=Duration.hours(1),
        )
        v1_method = v1_resource.add_method(
            "GET",
            aws_apigateway.LambdaIntegration(self.lambda_function),
            api_key_required=True,
        )
        api_resource = v1_resource.add_resource("{path+}")
        api_resource.add_cors_preflight(
            allow_origins=aws_apigateway.Cors.ALL_ORIGINS,
            allow_methods=aws_apigateway.Cors.ALL_METHODS,
            max_age=Duration.hours(1),
        )
        api_method = api_resource.add_method(
            "ANY",
            aws_apigateway.LambdaIntegration(self.lambda_function),
            api_key_required=True,
        )

        usage_plan.add_api_stage(
            stage=api_gateway.deployment_stage,
            throttle=[
                aws_apigateway.ThrottlingPerMethod(
                    method=v1_method,
                    throttle=aws_apigateway.ThrottleSettings(
                        burst_limit=50,
                        rate_limit=100,
                    ),
                ),
                aws_apigateway.ThrottlingPerMethod(
                    method=api_method,
                    throttle=aws_apigateway.ThrottleSettings(
                        burst_limit=50,
                        rate_limit=100,
                    ),
                ),
            ],
        )

        return api_gateway
