import aws_cdk as core
import aws_cdk.assertions as assertions

from deployment.simple_threads_stack import SimpleThreadsStack


# example tests. To run these tests, uncomment this file along with the example
# resource in deployment/simple_threads_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SimpleThreadsStack(app, "simple-threads")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
