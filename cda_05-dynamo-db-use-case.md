Let's walk through the steps required to implement this use case for Let's Go! Media Inc. on AWS, both through the AWS Management Console and then with AWS CLI commands.

### **Step 1: Create a DynamoDB Table Named `MediaCatalog`**

1. **Log in to the AWS Management Console** and navigate to the DynamoDB service.
2. **Create a new table**:
   - **Table name**: `MediaCatalog`
   - **Partition key**: `Title` (String)
   - Leave the other settings as default (No sort key, and use the default settings for read/write capacity).
3. Click **Create table**.

### **Step 2: Add 10 Latest Movie Releases to the `MediaCatalog` Table**

1. Once the table is created, select the `MediaCatalog` table from the list of tables.
2. Go to the **Items** tab and click on **Create item**.
3. Add each movie manually by filling in the following attributes:
   - `Title` (Partition key): Name of the movie (e.g., *Movie 1*)
   - `Genre`: e.g., Action, Drama, Comedy, etc.
   - `ReleaseDate`: e.g., `2023-08-15`
   - `Rating`: e.g., `8.0`

Repeat this process for 10 different movies.

### **Step 3: Create a t2.micro EC2 Instance**

1. Navigate to the **EC2 Dashboard** and click on **Launch Instance**.
2. **Configure the instance**:
   - **Name**: `MediaCatalogReader`
   - **Instance type**: `t2.micro`
   - **AMI**: Choose a basic Amazon Linux 2 AMI
   - **Key pair**: Select an existing key pair or create a new one for SSH access.
   - **Network settings**: Use the default VPC and subnet.
   - **Storage**: Use the default storage settings.
   - **Security group**: Create a new security group that allows SSH access from your IP address.

3. Click **Launch instance**.

### **Step 4: Create an IAM Role and Attach it to the EC2 Instance**

1. Go to the **IAM Dashboard** and select **Roles**.
2. Click **Create role**:
   - **Trusted entity**: AWS service
   - **Use case**: EC2
3. Click **Next: Permissions** and attach the `AmazonDynamoDBReadOnlyAccess` policy to the role.
4. **Name the role**: `MediaCatalogReadOnlyRole` and click **Create role**.
5. Go back to your EC2 instance:
   - Select your instance, click on **Actions > Security > Modify IAM Role**.
   - Attach the `MediaCatalogReadOnlyRole` to the instance.

### **Step 5: Use the AWS CLI on the EC2 Instance to Scan the `MediaCatalog` Table**

1. **SSH into your EC2 instance**:
   - Use the key pair you specified during the creation of the instance.
   - Example: `ssh -i your-key.pem ec2-user@<EC2-Instance-Public-IP>`

2. **Install the AWS CLI** (if it's not already installed):
   ```bash
   sudo yum update -y
   sudo yum install -y aws-cli
   ```

3. **Scan the DynamoDB table**:
   ```bash
   aws dynamodb scan --table-name MediaCatalog --region <your-region>
   ```

   This command should return the items in the `MediaCatalog` table.

### **Step 6: Validate Security by Attempting to Write to the `MediaCatalog` Table**

1. Try to add an item to the `MediaCatalog` table using the following command:
   ```bash
   aws dynamodb put-item --table-name MediaCatalog --item '{"Title": {"S": "Unauthorized Movie"}, "Genre": {"S": "Thriller"}, "ReleaseDate": {"S": "2024-01-01"}, "Rating": {"N": "8.5"}}' --region <your-region>
   ```

   You should receive an `AccessDeniedException`, confirming that your IAM role only has read permissions, and write operations are denied.

### **Conclusion**

I have successfully set up a secure DynamoDB table named `MediaCatalog` for Let's Go! Media Inc., allowing authorized users to retrieve information about the company's latest movie releases using an EC2 instance with appropriate IAM role permissions. The security of the setup was validated by confirming that unauthorized write attempts to the DynamoDB table are denied, ensuring the integrity of the media catalog data.

### ADVANCED ###
Using AWS CLI:

# Step 1: Create a DynamoDB Table Named `MediaCatalog`
```
aws dynamodb create-table \
    --table-name MediaCatalog \
    --attribute-definitions AttributeName=Title,AttributeType=S \
    --key-schema AttributeName=Title,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --region us-east-1
```

# Step 2: Add 10 Latest Movie Releases to the `MediaCatalog` Table
Here are the commands to add each of the 10 movies:
```
aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "Dune"},
        "Genre": {"S": "Sci-Fi, Adventure"},
        "ReleaseDate": {"S": "2021-10-22"},
        "Rating": {"N": "8.1"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "The Batman"},
        "Genre": {"S": "Action, Crime"},
        "ReleaseDate": {"S": "2022-03-04"},
        "Rating": {"N": "7.9"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "Top Gun: Maverick"},
        "Genre": {"S": "Action, Drama"},
        "ReleaseDate": {"S": "2022-05-27"},
        "Rating": {"N": "8.4"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "Black Panther: Wakanda Forever"},
        "Genre": {"S": "Action, Drama"},
        "ReleaseDate": {"S": "2022-11-11"},
        "Rating": {"N": "7.2"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "Everything Everywhere All at Once"},
        "Genre": {"S": "Action, Comedy"},
        "ReleaseDate": {"S": "2022-03-25"},
        "Rating": {"N": "8.1"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "The Irishman"},
        "Genre": {"S": "Biography, Crime"},
        "ReleaseDate": {"S": "2019-11-27"},
        "Rating": {"N": "7.8"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "1917"},
        "Genre": {"S": "Drama, War"},
        "ReleaseDate": {"S": "2019-12-25"},
        "Rating": {"N": "8.3"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "Tenet"},
        "Genre": {"S": "Action, Sci-Fi"},
        "ReleaseDate": {"S": "2020-09-03"},
        "Rating": {"N": "7.5"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "Nomadland"},
        "Genre": {"S": "Drama"},
        "ReleaseDate": {"S": "2020-12-04"},
        "Rating": {"N": "7.3"}
    }' \
    --region us-east-1

aws dynamodb put-item \
    --table-name MediaCatalog \
    --item '{
        "Title": {"S": "Oppenheimer"},
        "Genre": {"S": "Biography, Drama"},
        "ReleaseDate": {"S": "2023-07-21"},
        "Rating": {"N": "8.3"}
    }' \
    --region us-east-1
```

# Step 3: Create a t2.micro EC2 Instance
Using the provided AMI ID for Amazon Linux 2:

```
aws ec2 run-instances \
    --image-id ami-0c8e23f950c7725b9 \
    --instance-type t2.micro \
    --key-name EC2Tutorial\
    --security-group-ids sg-009b9d440ed9964ad \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MediaCatalogReader}]' \
    --region us-east-1
```

# Step 4: Create an IAM Role and Attach it to the EC2 Instance
Create the IAM role and attach the policy:

```
aws iam create-role \
    --role-name MediaCatalogReadOnlyRole \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    }'
```

Attach the DynamoDB read-only policy:

```
aws iam attach-role-policy \
    --role-name MediaCatalogReadOnlyRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess
```

Create the instance profile and associate it with the role:
```
aws iam create-instance-profile \
    --instance-profile-name MediaCatalogInstanceProfile
```

Add the role to the instance profile:

```
aws iam add-role-to-instance-profile \
    --instance-profile-name MediaCatalogInstanceProfile \
    --role-name MediaCatalogReadOnlyRole
```

Attach the instance profile to your EC2 instance:

```
aws ec2 associate-iam-instance-profile \
    --instance-id <your-instance-id> \
    --iam-instance-profile Name=MediaCatalogInstanceProfile \
    --region us-east-1
```

# Step 5: Use the AWS CLI on the EC2 Instance to Scan the `MediaCatalog` Table
SSH into the EC2 instance:

```
ssh -i EC2Tutorial.pem ec2-user@<EC2-Instance-Public-IP>
```

Once logged in, run:

```
aws dynamodb scan --table-name MediaCatalog --region us-east-1
```

# Step 6: Validate Security by Attempting to Write to the MediaCatalog Table
Try to add an unauthorized item:

```
aws dynamodb put-item --table-name MediaCatalog --item '{"Title": {"S": "Unauthorized Movie"}, "Genre": {"S": "Thriller"}, "ReleaseDate": {"S": "2024-01-01"}, "Rating": {"N": "8.5"}}' --region us-east-1
```

This should return an AccessDeniedException, confirming that the role only has read permissions.


####################################
############# COMPLEX ##############
#####################################

Creating a DynamoDB table, attaching an IAM role, and launching an EC2 instance using a CloudFormation template is a powerful way to automate the setup. Here’s how you can do it.

### CloudFormation Template Overview

The CloudFormation template will:
1. **Create a DynamoDB Table** named `MediaCatalog`.
2. **Create an IAM Role** with `AmazonDynamoDBReadOnlyAccess`.
3. **Launch a t2.micro EC2 Instance** with the IAM Role attached.

### CloudFormation Template

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: CloudFormation template to create a DynamoDB table, IAM role, and EC2 instance.

Resources:
  
  MediaCatalogDynamoDBTable:
    Type: "AWS::DynamoDB::Table"
    Properties: 
      TableName: "MediaCatalog"
      AttributeDefinitions: 
        - AttributeName: "Title"
          AttributeType: "S"
      KeySchema: 
        - AttributeName: "Title"
          KeyType: "HASH"
      ProvisionedThroughput: 
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5

  MediaCatalogRole:
    Type: "AWS::IAM::Role"
    Properties: 
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: "Allow"
            Principal:
              Service: "ec2.amazonaws.com"
            Action: "sts:AssumeRole"
      Path: "/"
      Policies:
        - PolicyName: "MediaCatalogDynamoDBReadOnlyPolicy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: "Allow"
                Action:
                  - "dynamodb:Scan"
                  - "dynamodb:Query"
                  - "dynamodb:GetItem"
                  - "dynamodb:BatchGetItem"
                Resource: "*"

  MediaCatalogInstanceProfile:
    Type: "AWS::IAM::InstanceProfile"
    Properties:
      Path: "/"
      Roles: 
        - Ref: "MediaCatalogRole"

  MediaCatalogEC2Instance:
    Type: "AWS::EC2::Instance"
    Properties:
      InstanceType: "t2.micro"
      ImageId: "ami-0c8e23f950c7725b9"  # Amazon Linux 2 AMI ID for us-east-1
      KeyName: "EC2Tutorial"  # Replace with your actual key pair name
      IamInstanceProfile: 
        Ref: "MediaCatalogInstanceProfile"
      SecurityGroupIds: 
        - "sg-009b9d440ed9964ad"  # Replace with your actual security group ID
      Tags:
        - Key: "Name"
          Value: "MediaCatalogReader"

Outputs:
  InstanceId:
    Description: "Instance ID of the newly created EC2 instance"
    Value: !Ref MediaCatalogEC2Instance
  TableName:
    Description: "DynamoDB Table Name"
    Value: !Ref MediaCatalogDynamoDBTable
```

### Steps to Deploy the CloudFormation Template

1. **Save the Template**:
   - Save the above YAML content to a file named `media-catalog-stack.yaml`.

2. **Deploy the CloudFormation Stack**:
   - Use the AWS CLI to deploy the CloudFormation stack.

   ```bash
   aws cloudformation create-stack --stack-name MediaCatalogStack --template-body file://media-catalog-stack.yaml --capabilities CAPABILITY_NAMED_IAM --region us-east-1
   ```

   - `--capabilities CAPABILITY_NAMED_IAM` is required because the stack is creating IAM resources.

3. **Monitor the Stack Creation**:
   - You can monitor the stack creation process via the AWS Management Console under the CloudFormation section or using the AWS CLI:

   ```bash
   aws cloudformation describe-stacks --stack-name MediaCatalogStack --region us-east-1
   ```

4. **Get Output Values**:
   - After the stack is successfully created, you can retrieve the outputs:

   ```bash
   aws cloudformation describe-stacks --stack-name MediaCatalogStack --query "Stacks[0].Outputs" --region us-east-1
   ```

### Customizing the Template

- **KeyName**: Make sure the `KeyName` in the EC2 instance properties matches an existing key pair in your AWS account.
- **SecurityGroupIds**: Replace `"sg-009b9d440ed9964ad"` with your actual security group ID that allows SSH access.
- **ImageId**: The AMI ID is specific to the `us-east-1` region. If you're using a different region, replace it with the corresponding AMI ID.

### Conclusion

This CloudFormation template automates the creation of a DynamoDB table, an IAM role, and an EC2 instance. Deploying this stack will set up your environment without requiring manual intervention. If you encounter any issues or need further customization, feel free to ask!