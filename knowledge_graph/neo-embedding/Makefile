.ONESHELL:
.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[35m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build
build:  ## Run `mvn` and build the docker image with the version: make build VERSION=0.0.1
	@mvn clean install -DskipTests
	@cp target/nembedding-$(VERSION).jar .
	docker build -t neo-embedding:$(VERSION) --build-arg="VERSION=$(VERSION)" .

.PHONY: push
push:  ## push the image to nexus: make build VERSION=0.0.1
	docker tag neo-embedding:$(VERSION) "localhost:8082/docker-private/neo-embedding:$(VERSION)"; \
        docker push "localhost:8082/docker-private/neo-embedding:$(VERSION)"

.PHONY: run
run:  ## Run the built docker locally: make run VERSION=0.0.1
	docker run \
        -p 7474:7474 -p 7687:7687 \
        -v $PWD/data:/data \
        --name neo-embedding \
        -e NEO4J_apoc_export_file_enabled=true \
        -e NEO4J_apoc_import_file_enabled=true \
        -e NEO4J_apoc_import_file_use__neo4j__config=true \
        -e NEO4J_PLUGINS=\[\"apoc-extended\"\] \
        neo-embedding:$(VERSION)
