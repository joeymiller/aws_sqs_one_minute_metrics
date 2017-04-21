import boto3, os

def lambda_handler(event, context):
    sqs = boto3.resource('sqs')
    cloudwatch = boto3.client('cloudwatch')
    queue_name = os.getenv('queue_name')
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    
    # Send to Custom SQS Metrics
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'Approximate Number Of Messages',
                'Dimensions': [
                    {
                        'Name': 'Queue Name',
                        'Value': queue_name.upper()
                    },
                ],
                'Unit': 'None',
                'Value': float(queue.attributes.get('ApproximateNumberOfMessages'))
            },
        ],
        Namespace='Custom SQS Metrics'
    )
    return queue.attributes.get('ApproximateNumberOfMessages')