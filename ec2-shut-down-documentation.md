Below is a complete Markdown document outlining the entire project, including creating the Lambda function, launching EC2 instances for testing, and cleaning up once you're done. You can copy this into a `.md` file for a blog post, documentation, or a GitHub repository.

```markdown
# Automating EC2 Shutdown with AWS Lambda

## Project Overview

This project demonstrates how to use an AWS Lambda function to automatically stop EC2 instances that are running past a specific time (7:00 PM EST) to help manage cloud costs. It covers setting up the Lambda function, testing the function by launching EC2 instances, and cleaning up the resources once the tests are complete.

### Prerequisites

Ensure you have the following prerequisites:
- **AWS Account**: Ensure you have access to an AWS account.
- **AWS CLI Installed and Configured**: Install the AWS CLI and authenticate it with your AWS account.
  - [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- **IAM Role for Lambda**: You'll need a role with permissions for `ec2:DescribeInstances` and `ec2:StopInstances`. If you haven't already set up the necessary IAM role, follow the steps below to create one.

---

## Part 1: Creating the Lambda Function

### Step 1: Set Up Lambda Function in AWS Console

1. **Log in to AWS Management Console** and go to the Lambda service.
2. **Click on “Create Function”**, select “Author from scratch.”
3. Name your function, for example, `StopEC2InstancesAfterHours`.
4. Select **Python 3.8** or higher as the runtime.
5. **Execution Role**: Choose an existing role with EC2 permissions or create a new role with the following permissions:
   - `ec2:DescribeInstances`
   - `ec2:StopInstances`

### Step 2: Lambda Function Code

Below is the Python code for the Lambda function that stops EC2 instances running past 7:00 PM EST. This code is designed to check the current time and stop instances that are running.

```python
import boto3
from datetime import datetime, timedelta, timezone
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
    
    # Adjust for EST (UTC-5, adjust for daylight savings manually if needed)
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
```

### Step 3: Schedule the Lambda Function

1. **Go to CloudWatch** in the AWS Management Console.
2. Select **Rules** under the Events section and click **Create Rule**.
3. Under **Event Source**, choose **Schedule** and set the expression to trigger the Lambda function daily at 7:00 PM EST.
   - Cron expression for 7:00 PM EST: `cron(0 0 23 * * ? *)`
4. Under **Targets**, select the Lambda function created above (`StopEC2InstancesAfterHours`).

---

## Part 2: Launching EC2 Instances for Testing

### Step 1: Launch EC2 Instances Using AWS CLI

To test the Lambda function, you'll need running EC2 instances. Launch 5 `t2.micro` EC2 instances using the AWS CLI:

```bash
aws ec2 run-instances \
    --image-id ami-0182f373e66f89c85 \
    --instance-type t2.micro \
    --count 5 \
    --key-name YourKeyPairName \
    --security-group-ids YourSecurityGroupID \
    --subnet-id YourSubnetID \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=DevLabInstance}]' \
    --associate-public-ip-address
```

- Replace `YourKeyPairName`, `YourSecurityGroupID`, and `YourSubnetID` with the appropriate values.
- This command launches 5 EC2 instances tagged as `DevLabInstance`.

### Step 2: Verify EC2 Instances

To verify that the instances have been launched, run the following command:

```bash
aws ec2 describe-instances --filters "Name=instance-state-name,Values=pending,running"
```

This command will list all the EC2 instances in the `pending` or `running` state.

---

## Part 3: Testing the Lambda Function

### Step 1: Manually Trigger Lambda Function

You can manually trigger the Lambda function to stop EC2 instances. To do this, go to the **AWS Lambda console**, select the function, and click **Test**.

1. Create a test event (you can use a blank template).
2. Invoke the Lambda function.

### Step 2: Verify that EC2 Instances Stopped

After triggering the Lambda function, you can verify if the instances have been stopped by running:

```bash
aws ec2 describe-instances --filters "Name=instance-state-name,Values=stopped"
```

This will list any EC2 instances that are in the `stopped` state.

---

## Part 4: Cleaning Up Resources

### Step 1: Terminate EC2 Instances

Once you're done testing, it's important to terminate the EC2 instances to avoid unnecessary charges. You can do this by running:

```bash
aws ec2 terminate-instances --instance-ids <instance-id-1> <instance-id-2> <instance-id-3> <instance-id-4> <instance-id-5>
```

Replace the placeholders with the actual instance IDs of the EC2 instances you launched.

### Step 2: Disable or Delete Lambda and CloudWatch Rule

If you no longer need the Lambda function, you can disable or delete the CloudWatch rule that triggers the function.

1. **Go to CloudWatch** and find the rule you created to trigger the Lambda function.
2. Disable or delete the rule.

You can also delete the Lambda function if you no longer need it by going to the **Lambda console** and selecting **Delete**.

---

## Conclusion

By following these steps, you've successfully created an automated solution to stop EC2 instances running past 7:00 PM EST. This solution can help manage cloud costs, ensuring that unused instances are not left running. You also learned how to set up the environment for testing and clean up resources when finished.

### Next Steps:
- Consider refining the Lambda function to handle more complex scheduling needs.
- Implement logging and monitoring to track the effectiveness of the solution in production.
- Experiment with scaling this approach to handle more complex AWS environments.
```

---

This Markdown file outlines the entire project from creating the Lambda function to launching and testing EC2 instances, as well as cleaning up resources after testing. You can now use it for your documentation, blog, or submission to a project repository.

Let me know if you'd like to add or modify anything else!