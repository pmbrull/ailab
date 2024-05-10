.ONESHELL:
.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[35m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: serve
serve:  ## Build the docker images
	@bentoml serve llm:LLM

.PHONY: build
build:  ## Build the docker images
	@bentoml build -f bentofile.yaml --containerize

.PHONY: push
push:  ## Push the docker images
	@BENTO_VERSION=$$(bentoml get llm:latest -o json | jq -r ".version"); \
	    docker tag "llm:$$BENTO_VERSION" "localhost:8082/docker-private/llm:$$BENTO_VERSION"; \
	    docker push "localhost:8082/docker-private/llm:$$BENTO_VERSION"
