Certainly! I'll walk you through the process of setting up a CI/CD pipeline using AWS CodePipeline to automate the deployment of a static website. Below are the steps to achieve this:

### Step 1: Create a Git Repository
1. **GitHub or CodeCommit**: 
   - **GitHub**:
     - Go to [GitHub](https://github.com/) and log in.
     - Click on `+` in the top-right corner and select `New repository`.
     - Name your repository (e.g., `static-website`), add a description, and set the repository to public or private.
     - Click `Create repository`.
   - **AWS CodeCommit**:
     - Go to the AWS Management Console and navigate to CodeCommit.
     - Click `Create repository`.
     - Name the repository (e.g., `static-website`) and provide a description.
     - Click `Create`.

2. **Load HTML Content**:
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/your-username/static-website.git
     # or for CodeCommit
     git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/static-website
     ```
   - Add the HTML content to the repository.
   - Commit and push the changes:
     ```bash
     git add .
     git commit -m "Initial commit with HTML content"
     git push origin main
     ```

### Step 2: Create and Configure an S3 Bucket
1. **Create an S3 Bucket**:
   - Navigate to the S3 service in the AWS Management Console.
   - Click `Create bucket`.
   - Name the bucket (e.g., `my-static-website-bucket`).
   - Choose a region and configure settings as required.
   - Uncheck `Block all public access` under the `Object Ownership` and `Public access settings` sections if you want your website to be public.
   - Click `Create bucket`.

2. **Configure the Bucket for Static Website Hosting**:
   - Go to your S3 bucket and click `Properties`.
   - Scroll down to `Static website hosting` and click `Edit`.
   - Enable `Static website hosting`.
   - Specify the `Index document` (e.g., `index.html`).
   - Optionally specify an `Error document` (e.g., `error.html`).
   - Click `Save changes`.

3. **Set Permissions**:
   - Go to the `Permissions` tab and click `Bucket Policy`.
   - Add a bucket policy to allow public access (if your website is public):
     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Sid": "PublicReadGetObject",
           "Effect": "Allow",
           "Principal": "*",
           "Action": "s3:GetObject",
           "Resource": "arn:aws:s3:::my-static-website-bucket/*"
         }
       ]
     }
     ```
   - Replace `my-static-website-bucket` with your bucket name.
   - Click `Save`.

### Step 3: Create a CI/CD Pipeline Using AWS CodePipeline
1. **Navigate to CodePipeline**:
   - Go to the AWS Management Console and navigate to the CodePipeline service.
   - Click `Create pipeline`.

2. **Pipeline Settings**:
   - Name your pipeline (e.g., `static-website-pipeline`).
   - Choose a new service role or use an existing one.
   - Click `Next`.

3. **Add Source Stage**:
   - Choose `GitHub` or `AWS CodeCommit` as the source provider.
   - If using GitHub, connect to your GitHub account.
   - Choose the repository you created (e.g., `static-website`) and select the branch (e.g., `main`).
   - Click `Next`.

4. **Add Build Stage** (Optional):
   - If you're only deploying static content without any build process, you can skip this stage. Otherwise, configure a build project using CodeBuild.

5. **Add Deploy Stage**:
   - Choose `Amazon S3` as the deployment provider.
   - Select your S3 bucket (`my-static-website-bucket`).
   - Specify the `Extract file before deploy` option if your repository is zipped.
   - Click `Next`.

6. **Review and Create**:
   - Review your pipeline settings.
   - Click `Create pipeline`.

### Step 4: Deploy the Pipeline
- Once the pipeline is created, it will automatically trigger based on the repository's state.
- The pipeline will fetch the latest code, and if a build stage is included, it will build the project, then deploy the HTML content to the S3 bucket.

### Step 5: Verify the Static Website
- After deployment, navigate to the S3 bucket URL to verify the website.
- The URL format is `http://my-static-website-bucket.s3-website-us-east-1.amazonaws.com`, where `us-east-1` is your bucket's region.

### Step 6: Make a Code Update to Trigger the Pipeline
1. **Modify the Code**:
   - Make a simple change to the HTML file, like changing some text.
   - Commit and push the change to the repository:
     ```bash
     git add .
     git commit -m "Updated the website content"
     git push origin main
     ```

2. **Verify Pipeline Trigger**:
   - The pipeline should trigger automatically due to the code change.
   - Once the pipeline finishes, check the S3 bucket URL to confirm that the changes have been deployed successfully.

By following these steps, you've set up a fully automated CI/CD pipeline for your static website using AWS CodePipeline, GitHub (or CodeCommit), and S3.

Great to hear that the previous issue is resolved! Let's move on to implementing the advanced features: adding a manual approval step to the pipeline and setting up a CloudFront distribution to reduce latency.

### 1. **Adding a Manual Approval Step to CodePipeline**

To add a manual approval step, you'll include an "Approval" action between the build (or source) and deploy stages in your pipeline. Here's how to do it:


###############################################################################################################################################################
###############################################################################################################################################################
#### Steps to Add Manual Approval:
1. **Navigate to CodePipeline**:
   - Go to the AWS Management Console and open CodePipeline.

2. **Edit the Pipeline**:
   - Select your pipeline (e.g., `static-website-pipeline`).
   - Click on "Edit".

3. **Add a Manual Approval Stage**:
   - Click on "Add stage" between the build/source stage and the deploy stage.
   - Name the stage something like `Approval`.

4. **Add Approval Action**:
   - Inside the new stage, click "Add action".
   - Set the `Action name` to something like `ManualApproval`.
   - For `Action provider`, select `Manual approval`.
   - Set the `Approval notification ARN` to the ARN of an SNS topic that the senior developer is subscribed to. If you don’t have an SNS topic yet, you can create one and subscribe the senior developer’s email to it.
   - Optionally, add a message or URL that will be included in the approval request.

5. **Save and Deploy**:
   - After configuring the approval action, save your changes and deploy the pipeline.

Now, whenever a change is made and the pipeline runs, it will pause at the manual approval stage, and the designated senior developer will receive an email notification to approve or reject the deployment.

### 2. **Setting Up a CloudFront Distribution**

To improve the latency of your website, you can set up an Amazon CloudFront distribution that serves content from your S3 bucket globally through edge locations.

#### Steps to Set Up CloudFront:
1. **Navigate to CloudFront**:
   - Go to the AWS Management Console and open CloudFront.

2. **Create a New Distribution**:
   - Click on `Create distribution`.
   - Choose `Web` as the distribution type.

3. **Configure the Origin**:
   - For the `Origin domain name`, select your S3 bucket (`static-website-bucket-aug-2024`).
   - Set the `Origin Path` to `/` or leave it blank if you're pointing directly to the root.
   - **S3 Bucket as an Origin**: Set the `Origin access control settings` according to your requirements. If the bucket should be private and accessible only via CloudFront, configure an Origin Access Control (OAC) and update your bucket policy accordingly.

4. **Configure Default Cache Behavior**:
   - Set the `Viewer Protocol Policy` to `Redirect HTTP to HTTPS` to enforce secure connections.
   - Configure caching and TTL settings based on your needs. The default settings are usually fine for a basic static website.

5. **Set Distribution Settings**:
   - Under `Distribution settings`, set a custom domain name if you have one, otherwise, you can use the default CloudFront domain.
   - If you have a custom domain, configure an SSL certificate through AWS Certificate Manager (ACM).

6. **Create the Distribution**:
   - Review your settings and click `Create distribution`.

7. **Update DNS (Optional)**:
   - If you’re using a custom domain, update your DNS settings to point to the CloudFront distribution. This typically involves creating a CNAME record in your DNS provider’s console.

### 3. **Testing and Verification**
- Once the CloudFront distribution is created, test the website using the CloudFront domain name.
- Verify that the website loads correctly and that latency is reduced. You can use tools like `ping`, `traceroute`, or online services like GTMetrix to measure improvements.

### Summary of the Advanced Setup:
- **Manual Approval**: Added a manual approval stage to your CodePipeline to ensure changes are reviewed by a senior developer before deployment.
- **CloudFront Distribution**: Configured a CloudFront distribution to improve website latency and enhance global performance.

After these implementations, your pipeline will be more robust, and your website performance should see a noticeable improvement. Let me know if you have any questions or need further assistance!