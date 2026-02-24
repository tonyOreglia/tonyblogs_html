---
date: '2023-07-31'
draft: true
title: 'Publishing to SNS Topic from Lambda Using VPC Endpoint with SAM Template: AWS Serverless Application Model (SAM) Pub/Sub Architecture'
tags:
- AWS
- serverless
- software development
- technology
---

Amazon Web Services provides a multitude of tools for developers to build robust and scalable cloud applications. In this article, I’ll guide you through publishing to a Simple Notification Service (SNS) topic from a Lambda function through a VPC Endpoint. We’ll encode this architecture using the AWS Serverless Application Model (SAM) toolset.

This setup is part of a Pub/Sub architecture which offers several benefits:

1. **Better Security**: Placing the Lambda function within a Virtual Private Cloud (VPC) through a VPC Endpoint ensures that the communication between the Lambda function and SNS topic remains private, isolated from the public internet, and protected from unauthorized access.
2. **Performance Improvement**: Directly accessing SNS through a VPC Endpoint often results in lower latencies since the communication stays within the AWS network infrastructure. Also, in general, the Pub/Sub architecture enables untethers the function from downstream side-effects. This relieves the function from the latency and error handling responsibility for these side effects which directly improves the user experience.
3. **Scalability and Flexibility**: The pub-sub architecture scales to varying workloads effectively. SNS can handle thousands of messages being published concurrently and the downstream Lambda consumers scale automatically.

### In this tutorial, we will discuss
1. Briefly what AWS Lambda, SNS, and VPC endpoints are.
1. How to configure a VPC endpoint.
1. How to publish messages to SNS from Lambda using the configured VPC endpoint.
1. Code snippets of AWS SAM templates.

## What Are AWS Lambda, SNS, and VPC endpoints?
Before diving into the practical aspect of this article, let’s briefly review the building blocks we’ll be using:

- **AWS Lambda**: This is a serverless compute service that lets you run your code without provisioning or managing servers. It executes your code only when needed and scales automatically.
- **AWS SNS (Simple Notification Service)**: SNS is a fully managed messaging service. The pub/sub messages can fan out to a large number of subscribers.
- **VPC Endpoint**: This allows you to privately connect your VPC to supported AWS services and VPC endpoint services.

## Setting up the VPC Endpoint
The first step is to set up the VPC endpoint for Amazon SNS. Here’s an AWS SAM snippet that shows how you can create a VPC endpoint, subnet, and a basic Security Group for Amazon SNS:

```yaml
Resources:

  SnsVpcEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcEndpointType: Interface
      PrivateDnsEnabled: true
      ServiceName: com.amazonaws.<REGION>.sns
      VpcId: <VPC-ID>
      SubnetIds:
        - !Ref PrivateSubnetForSnsDefaultVpc
      SecurityGroupIds: # Create a security group and allow all inbound access from the VPC CIDR
        - !Ref SnsVpcEndpointSecurityGroup

  PrivateSubnetForSnsDefaultVpc:
    Type: AWS::EC2::Subnet
    Properties:
      AvailabilityZone: us-east-1c
      CidrBlock: <CIDR-BLOCK>
      VpcId: <VPC-ID>
      MapPublicIpOnLaunch: false

  SnsVpcEndpointSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Security Group for SNS VPC Endpoint
      VpcId: <VPC-ID>
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: <VPC-CIDR-BLOCK>
```

Replace <REGION>,<VPC-ID>, <VPC-CIDR-BLOCK> and <CIDR-BLOCK> with your actual values. For <VPC-ID> I use the AWS default VPC which can be retrieved from the UI.

Let’s break down each of these resources.

### ECS::Security Group
This controls the traffic that to and from the VPC Endpoint being created.

Egress is not defined here. By default, when you create an EC2 Security Group, all outbound traffic is allowed.

### EC2::Subnet
A subnet is like a partition within a larger network (VPC) that allows you to isolate resources. Instances launched in this subnet won’t get a public IP address by default because **MapPublicIpOnLaunch** is set to **false**.

The **CIDR-BLOCK** should fall within the VPC’s range and **should not overlap with any other subnet CIDR blocks**. There are some nice tools online to help you visualize and choose non-overlapping CIDR blocks. For example, https://cidr.xyz/.

### EC2::VPCEndpoint
A VPC endpoint for Amazon SNS enables you to privately connect your VPC to SNS without requiring an internet gateway, a VPN connection, or AWS Direct Connect.

### Creating the AWS Lambda Function
Let’s now create a Lambda function that will publish messages to an SNS topic. We will write this function in Node.js. Note that you need to provide appropriate IAM permissions to the Lambda function to publish to the SNS topic.

Here is an AWS SAM snippet that shows how you can create the Lambda function:

```yaml
Resources:
  MyLambdaFunction:
    Type: 'AWS::Serverless::Function'
    Properties:
      CodeUri: s3://<bucket-name>/<code-zip>
      Handler: index.handler
      Runtime: nodejs14.x
      Environment: 
        Variables:
          SNS_TOPIC_ARN: !Ref SnsTopic
      VpcConfig:
        SubnetIds:
          - !Ref PrivateSubnetForSnsDefaultVpc
      Events:
        MyAPI:
          Type: Api
          Properties:
          Path: /test
          Method: post
      Policies:
        - SNSPublishMessagePolicy:
          TopicName: !Ref SnsTopic
```

Here, **<bucket-name>/<code-zip>** should be replaced with the actual S3 bucket name and the path to your Lambda function’s ZIP file.

Now let’s take a look at the actual Lambda function code:

```javascript
const AWS = require('aws-sdk');

exports.handler = async (event, context) => {
  // The endpoint is not needed when connecting to SNS from within a VPC
  const sns = new AWS.SNS();
  const topicArn = process.env.SNS_TOPIC_ARN;
  const message = 'Hello, SNS!';
  const params = {
    Message: message,
    TopicArn: topicArn
  };
  try {
    const publishResponse = await sns.publish(params).promise();
    console.log(`Message ${params.Message} sent to the topic ${params.TopicArn}`);
    console.log('MessageID is ' + publishResponse.MessageId);
    return publishResponse;
  } catch (error) {
    console.error(`Error publishing message ${params.Message} to topic ${params.TopicArn}`);
    console.error(error);
    throw error;
  }
};
```

This code receives an event, creates an SNS message, and then publishes it to the SNS topic. It logs the response from the SNS service or throws an error if the publish operation was not successful.

## Conclusion
In this article, we have seen how to configure AWS resources such as Lambda, SNS, and VPC endpoints using AWS SAM templates. We have also shown how you can publish messages to an SNS topic from a Lambda function. This setup is useful for developers building serverless applications that need to publish messages to an SNS topic from within a VPC. By setting up a VPC endpoint for SNS, you can ensure that your messages are published securely and privately without traversing the public internet.

Remember that while AWS SAM templates offer a quick and repeatable method for configuring your resources, it’s crucial to understand each component and customize it according to your specific use case and security considerations.

Good luck with your serverless journey!

---

Thanks for reading! I hope you've found something useful or interesting here.

Follow me on [Twitter](https://x.com/tony_oreglia) where I share my journey to $5k MRR.

Originally published on [Medium](https://tony-oreglia.medium.com/publishing-to-sns-topic-from-lambda-using-vpc-endpoint-with-sam-template-101794383403)
