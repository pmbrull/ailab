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
	ruff format .
	ruff --fix .
	ruff .

.PHONY: uv
uv:  ## Install https://github.com/astral-sh/uv
	@pip install --no-cache "uv~=0.1"

.PHONY: venv
venv:  ## Prepare the virtualenv with uv
	@uv venv