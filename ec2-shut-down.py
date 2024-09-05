import boto3
from datetime import datetime, timezone, timedelta
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize EC2 client
ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    # Define the target time for 7:00 PM EST (5 hours behind UTC, or 4 during daylight savings)
    target_hour = 19  # 7 PM in 24-hour format
    now_utc = datetime.now(timezone.utc)
    
    # Adjust for EST (UTC-5, adjust for daylight saving manually if needed)
    est_offset = timedelta(hours=-5)  # or -4 during daylight savings
    now_est = now_utc + est_offset
    
    # Check if it's past 7:00 PM EST
    if now_est.hour >= target_hour:
        try:
            # Describe all instances
            response = ec2.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            
            # List to hold instance IDs that will be stopped
            instances_to_stop = []

            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    instances_to_stop.append(instance_id)
                    logger.info(f'Instance {instance_id} is scheduled to stop.')

            # Stop the instances if any are running
            if instances_to_stop:
                ec2.stop_instances(InstanceIds=instances_to_stop)
                logger.info(f'Stopped instances: {instances_to_stop}')
            else:
                logger.info('No running instances found to stop.')
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
    
    else:
        logger.info('It is not yet 7:00 PM EST; no instances will be stopped.')

    return {
        'statusCode': 200,
        'body': 'Script executed successfully.'
    }
