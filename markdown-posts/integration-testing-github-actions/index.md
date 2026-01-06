---
title: "Tips for Integration Testing with GitHub Actions CI pipeline: AWS SAM Backend Integration Testing with GitHub Actions"
date: 2022-12-31
tags: 
- software engineering
- guides and tutorials
- programming
- AWS
- GitHub Actions
- testing
- CI/CD
---

![GitHub Actions CI Pipeline](https://miro.medium.com/v2/resize:fit:1400/1*5WC9rtIa0KLXfRrC8Swf1w.png)

This article contains some tips and code to help with adding Serverless Backend Integration tests to GitHub Actions.

Integrating tests into the CI pipeline improves confidence that existing behavior has not been broken by changes. Typically a production code base will have tests integrated into the CI, and any merge request must pass the tests before being merged and deployed to production.

Regarding the local implementation of AWS SAM backend integration tests, have a look at [this article](https://better-programming.pub/tips-and-tricks-for-testing-aws-sam-backend-infrastructure-8a0071f207ef).

Many of the following tips are generally applicable, however, this guide specifically covers testing Lambda functions triggered by API Gateway endpoint setup with an AWS SAM template with DynamoDB and S3 as databases. The tests are written in Jest. LocalStack is used to mock S3 and DymamoDB.

## Tip 1: Installing SAM and Node on the CI runner

GitHub Actions has some useful helper utilities for installing common tools used in CI pipelines. The following snippet exposes AWS SAM CLI to the CI runner.

```yaml
jobs:
  job1:
    steps:
      - uses: aws-actions/setup-sam@v2
```

Note that the above snippet is incomplete, the complete configuration is shared at the bottom.

## Tip 2: Installing Dependencies

Before tests can be run, external library dependencies need to be installed. In the case of a node module, you can use `npm clean-install` or just `npm ci` as a shorter alias. The clean install option is intended for CI environments; it will install exactly what is in `package-lock.json` without modification.

Often times there may be multiple packages involved in the project. For example, the test framework could be its own package, while the lambda functions have their own dependencies. Make sure to install all dependencies. You can use the `working-directory` parameter to set the directory to run the command from.

```yaml
jobs:
  job1:
    steps:
      - name: Install Lambda Dependencies
        run: npm ci
        working-directory: backend-serverless/lambda/dependencies/nodejs
      - run: npm ci
```

## Tip 3: AWS Credentials in the CI

The AWS SDK requires credentials to be attached for each request. Running tests locally, this requirement may be covered by a local was configuration file which will not be available on the CI runner. Note that, since the AWS dependencies are being mocked, a real credential is not necessary — but the SDK expects to have some string set for the credentials nonetheless. One way to solve this is to explicitly set dummy values for the AWS credentials in the test setup. For example, the following is sufficient to connect with DynamoDB mocked with Localstack.

```javascript
const dynamoDb = new AWS.DynamoDB({
  apiVersion: '2012-08-10',
  region: 'us-east-1',
  endpoint: 'http://localhost:4566',
  credentials: {
    accessKeyId: 'test',
    secretAccessKey: 'test'
  }
});
```

## Tip 4: Using the CI Environment Variable

There may be some other differences between running tests locally and on the CI runner. One useful environment variable that is automatically set to `true` on the CI runner is `CI`. Environment variables are accessible from a node process via `process.env.CI`. A full list of predefined variables can be found here: https://docs.gitlab.com/ee/ci/variables/predefined_variables.html.

## Tip 5: A Note about TMPDIR Environment Variable and LocalStack

This tip might save some people time. TMPDIR is an environment variable that is set on most Unix systems which points to a temporary directory. Often it is used for the Localstack HOST_TMP_FOLDER setting. On the GitHub CI runner, TMPDIR is not set by default, so make sure you provide a default in the docker-compose.yml configuration. For example

```yaml
version: '3.0'

services:

  localstack:
    image: localstack/localstack:latest
    environment:
      - AWS_DEFAULT_REGION=us-east-1
      - EDGE_PORT=4566
      - SERVICES=dynamodb,s3
      - KINESIS_PROVIDER=kinesalite
      - HOST_TMP_FOLDER=${TMPDIR:-/tmp}
      - MAIN_CONTAINER_NAME=localstack_main
      - LOCALSTACK_HOSTNAME=localhost
    ports:
      - "127.0.0.1:4566:4566"
    volumes:
      - "${TMPDIR:-/tmp/localstack}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
networks:
  default:
    external: true
    name: "localstack"
```

## Tip 6: Running AWS SAM Daemon within CI

You will want to run the AWS SAM local daemon within the CI environment for the tests. This can be a little tricky especially to make sure the daemon is killed when the tests are complete (which JEST requires to close out the tests daemon).

The process will need to be spawned in detached mode to ensure all child processes are part of the same process group. This enables killing the entire process group in the global teardown setup. Further, the process ID will need to be stored in global scope so it's available in the global teardown script. Lastly, the standard output events will need to be listened in on in order to ascertain when SAM Local has successfully started.

So for example, my global-setup.js script contains:

```javascript
const startAwsSamLocal = async () => {
  return new Promise((resolve, reject) => {
    let successfullyStartedSamLocal = false;
    var samLocalD = spawn(`${__dirname}/../Resources/run-sam-stack-local.sh`, ['default'], {
      // if options.detached is set to true, the child process will be made the leader of a new process group and session
      // this enables killing of the whole process group, see ./global-teardown.js
      detached: true,
      cwd: `${__dirname}/../Resources/`
    });
    console.log(`started AWS SAM Local daemon, process group ID: ${samLocalD.pid}`);

    globalThis.__AWS_SAM_LOCAL_D__ = samLocalD;
    samLocalD.stdout.setEncoding('utf8');
    samLocalD.stderr.setEncoding('utf8');

    samLocalD.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
    });

    samLocalD.stderr.on('data', (data) => {
      // I don't know why the sam cli is emitting to stderr
      if (data.includes(`Running on http://127.0.0.1`)) {
        console.log(data);
        successfullyStartedSamLocal = true;
        resolve();
      }
    });
  });
};
```

Which is only triggered if the CI env variable is true:

```javascript
if (process.env.CI) {
      console.log('starting AwsSamLocal');
      await startAwsSamLocal();
    }
```

Finally, the actual bash script which starts SAM stack locally looks like this;

```bash
#!/bin/bash
if [ $# -eq 0 ]; then
    export AWS_PROFILE=personal
fi

if ! docker network ls | grep localstack; then
    echo "creating localstack network"
    docker network create localstack; 
fi

sam local start-api \
    --parameter-overrides 'ParameterKey=CORSAllowOrigin,ParameterValue=http://127.0.0.1:3000' \
    --env-vars "$( dirname -- "$0"; )/local-sam-env.json" \
    --template "$( dirname -- "$0"; )/template.yaml" \
    --warm-containers 'EAGER' \
    --docker-network 'localstack' \
    --port 3001
```

## Tip 7: Stopping up AWS SAM Daemon

This approach enables a clean teardown script that uses the global scope variable to kill the SAM daemon process group:

```javascript
module.exports = async () => {
  // leave up dynamo and s3 on localstack; don't destroy the tables either
  // tear down SAM local stack

  // note '-' before pid. This converts a pid to a group of pids for process kill() method.
  // https://azimi.me/2014/12/31/kill-child_process-node-js.html
  // https://en.wikipedia.org/wiki/Process_group
  // https://linux.die.net/man/1/kill == "When an argument of the form '-n' is given, and it is meant to denote a process group"
  if (process.env.CI) {
    console.log('stopping AWS SAM Local');
    process.kill(-globalThis.__AWS_SAM_LOCAL_D__.pid);
  }
};
```

I hope you've found this article helpful!

## Resources

- https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-nodejs
- https://github.com/peter-evans/docker-compose-actions-workflow
- https://www.twilio.com/blog/working-with-environment-variables-in-node-js-html
- https://github.com/actions/setup-node
- https://docs.github.com/en/actions/using-workflows/about-workflows
- https://bobbyhadz.com/blog/aws-cli-config-profile-could-not-be-found
- https://discourse.nodered.org/t/connection-refused-to-aws-running-on-localstack/64941
- https://stackoverflow.com/questions/65289690/macos-env-tmpdir-notworking-in-github-actions
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/globalThis
- https://github.com/facebook/jest/issues/2441
- https://docs.localstack.cloud/user-guide/ci/github-actions/
- https://jestjs.io/docs/cli#--verbose
- https://github.com/localstack/localstack/blob/master/docker-compose.yml
- https://github.com/orgs/community/discussions/25742
- https://docs.npmjs.com/cli/v9/commands/npm-ci