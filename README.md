# Print-Rider

Simple Http APIs sharing using HttpRider. 

<demo>

### Architecture:

The PrintRider service is developed using the Python [Flask]() framework and deployed to [AWS Lambda]() with the [Serverless Framework]().

<diagram>

### Installation:

You need to have `docker` and `python3` available for building and running it locally.
If you are deploying to `AWS` then please make sure that you have the appropriate credentials under `printrider` profile.

There are several ways to start the application.

*Running locally with dynamodb in a docker container*

If running for the first time, `setup-local` will start DynamoDB in a docker container and setup the required table.

`make setup-local run-local`

*Running everything in docker using docker-compose*

This will build the current project and run Flask alongside DynamoDB in docker containers. 
Once the containers are running, `setup-local` will create the required table.
 
`make run-local-docker setup-local`

*Running using SAM local*

To simulate the environment as close to AWS Lambda as possible, the following command will use the [SAM CLI]() to start the Api locally.
Make sure that you are running DynamoDB locally using docker `make setup-local` as the docker container running SAM will try to connect to the same network.

`make run-local-sam`

*Testing when running locally*

The Application will come up on port 5000 when running locally, so it is easy to run the following curl commands to test it.

_Sharing a new API exchange_

This curl command will return the URL of the generated document in the location header.

```
echo '{"document": "c29tZXRoaW5n"}' | curl -H 'Content-Type: application/json' -d@- -v http://localhost:5000/prints
```

See [this](https://printrider.bettercallbots.com/prints/13a0ab45-65fb-4511-bc61-dedccb9742e1) for the full request/response.  

*Deploying to AWS*
Currently, it only supports two different stages when deploying to AWS. 
To prepare for the deployment, copy `.env.example` to `.env.beta` for dev deployment and `.env.prod` for live deployment. 

The `serverless` stack is also broken down in Infra services (DynamoDB setup) and API services (Api Gateway, Lambda etc)

Please note that running the following commands with a valid AWS profile will incur some charges depending on your AWS account.

_Dev_

todo

_Live_

todo

### Contributing:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License:
MIT