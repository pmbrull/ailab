.ONESHELL:
.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[35m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:  ## Run `mvn` and build the docker image with the version: make build VERSION=0.0.1
	@mvn install
	@cp target/nembedding-$(VERSION).jar .
	docker build -t neo-embedding:$(VERSION) .

.PHONY: push
push:  ## push the image to nexus: make build VERSION=0.0.1
	docker tag neo-embedding:$(VERSION) "localhost:8082/docker-private/neo-embedding:$(VERSION)"; \
        docker push "localhost:8082/docker-private/neo-embedding:$(VERSION)"
