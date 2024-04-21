.ONESHELL:
.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[35m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: precommit_install
precommit_install:  ## Install the project's precommit hooks from .pre-commit-config.yaml
	@echo "Installing pre-commit hooks"
	@echo "Make sure to first run install_dev first"
	@pre-commit install

.PHONY: lint
lint:  ## Run linter
	ruff --fix .
	ruff .

.PHONY: uv
uv:  ## Install https://github.com/astral-sh/uv
	@pip install --no-cache "uv~=0.1"

.PHONY: venv
venv:  ## Prepare the virtualenv with uv
	@uv venv

.PHONY: install
install:  ## Install the project
	@uv pip install .

.PHONY: install_dev
install_dev:  ## Install the dev dependencies
	@uv pip install ".[dev]"

.PHONY: build
build:  ## Build the docker images
	@cd embeddings && bentoml build -f bentofile.yaml --containerize

.PHONY: push
push:  ## Push the docker images
	@BENTO_VERSION=$(bentoml get transformer:latest -o json | jq ".version") && \
	    @docker push localhost:8082/docker-private/transformer:$$BENTO_VERSION"
