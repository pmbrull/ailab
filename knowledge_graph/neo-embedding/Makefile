.ONESHELL:
.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[35m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:  ## Run `mvn` and build the docker image
	mvn install
	cp target/nembedding-0.0.1-SNAPSHOT.jar .
	docker build -t neo-embedding .
