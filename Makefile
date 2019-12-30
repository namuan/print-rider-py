export PROJECTNAME=$(shell basename "$(PWD)")

.SILENT: ;               # no need for @

dynamo-local: ## Start local dynamo database
	docker-compose -f docker-compose-development.yml up -d dynamo

setup-local: dynamo-local ## Setup local environment (DynamoDb tables etc)
	aws dynamodb create-table --cli-input-json file://development/create-print-documents-table.json --endpoint-url http://localhost:8000

run-local: ## Runs the service locally connecting with dynamodb in Docker
	FLASK_ENV=development DEBUG=True AWS_SAM_LOCAL=True APP_DYNAMO=http://localhost:8000 python3 -m flask run

run-local-docker: ## Runs the service in docker
	docker-compose -f docker-compose.development.yml up -d --build

stop-local-docker: ## Stop docker containers and clean up
	docker-compose -f docker-compose.development.yml down --remove-orphans

test: ## Test the service locally connecting with dynamodb in Docker
	python -m pytest tests

run-local-sam: sls-package	## Runs the service locally with SAM
	sam local start-api --template development/sam.yaml --port 5000 --docker-network print-rider-py_default

prepare-sls-base: ## Installs NPM dependencies for Base infrastructure
	cd infra/base && npm install

deploy-sls-infra-base-dev: prepare-sls-base ## Deploy base infrastructure with Serverless framework
	cd infra/base && sls --config serverless.yml deploy -v

deploy-sls-infra-base-prod: prepare-sls-base ## Deploy base infrastructure with Serverless framework
	cd infra/base && sls --config serverless.yml deploy -v --stage prod

prepare-sls-functions: ## Installs NPM dependencies for Functions
	npm install

sls-package: ## Packages the source in a zip file
	sls --config serverless.yml package --stage dev --env local

deploy-sls-functions-dev: prepare-sls-functions ## Deploy functions infrastructure with Serverless framework
	sls --config serverless.yml deploy -v --stage dev --env beta

create-sls-domain-dev: prepare-sls-functions ## Deploy functions infrastructure with Serverless framework
	sls --config serverless.yml create_domain --stage dev -v --env beta

delete-sls-domain-dev: prepare-sls-functions ## Deploy functions infrastructure with Serverless framework
	echo "Are you sure about this? If yes then copy paste the following command"
	echo "sls --config serverless.yml delete_domain --stage dev -v --env beta"

remove-sls-functions-dev: prepare-sls-functions ## Deploy functions infrastructure with Serverless framework
	sls --config serverless.yml remove -v --stage dev --env beta

deploy-sls-functions-prod: prepare-sls-functions ## Deploy functions infrastructure with Serverless framework
	sls --config serverless.yml deploy -v --stage prod --env prod

create-sls-domain-prod: prepare-sls-functions ## Deploy functions infrastructure with Serverless framework
	sls --config serverless.yml create_domain --stage prod -v --env prod

delete-sls-domain-prod: prepare-sls-functions ## Deploy functions infrastructure with Serverless framework
	echo "Are you sure about this? If yes then copy paste the following command"
	echo "sls --config serverless.yml delete_domain --stage prod -v --env prod"

remove-sls-functions-prod: prepare-sls-functions ## Deploy functions infrastructure with Serverless framework
	sls --config serverless.yml remove -v --stage prod --env prod

lambda-app-logs-dev: ## Tail logs
	sls --config serverless.yml logs -f app -v --stage dev --env beta

lambda-app-logs-prod: ## Tail logs
	sls --config serverless.yml logs -f app -v --stage prod --env prod

.PHONY: help
.DEFAULT_GOAL := help

help: Makefile
	echo
	echo " Choose a command run in "$(PROJECTNAME)":"
	echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	echo