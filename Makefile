.PHONY: help install db dp dev start lint test image push docker-compose-start deploy-k8s doc pypi clean

# Variables
TAG ?= v1.1.1
RELEASE_NAME = fast-web
DOCKERHUB_USER = tyvek2zhang
SOURCE_DIR = src
SCRIPT_DIR = script
DOCS_DIR = docs
SERVER_LOG = server.log

help:
	@echo "Available make targets:"
	@echo "  install               Install project dependencies using uv"
	@echo "  db                    Generate db structure"
	@echo "  dp                    Upgrade db structure"
	@echo "  dev                   Development environment startup"
	@echo "  start                 Production environment startup"
	@echo "  lint                  Perform static code analysis"
	@echo "  test                  Run unit tests"
	@echo "  image                 Build the Docker image for the project"
	@echo "  push                  Push Docker image to dockerHub"
	@echo "  docker-compose-start  Start the project using Docker Compose"
	@echo "  deploy-k8s            Deploy the project to Kubernetes"
	@echo "  doc                   Generate documentation"
	@echo "  pypi                  Build and publish to PyPI"
	@echo "  clean                 Remove temporary files"
	@echo ""
	@echo "Use 'make <target>' to run a specific command."

install:
	uv sync

db:
	alembic revision --autogenerate

dp:
	alembic upgrade head

dev: install
	uv run alembic upgrade head && \
	uv run apiserver.py

start: install
	uv run alembic upgrade head && \
	nohup uvicorn apiserver.py --env prod > $(SERVER_LOG) 2>&1 &

lint:
	uv add pre-commit --group test && \
	pre-commit run --all-files --verbose --show-diff-on-failure

test:
	rm -rf $(SOURCE_DIR)/main/resource/alembic/db/fast_web.db; \
	rm -rf htmlcov; \
	uv sync --group dev; \
	alembic upgrade head; \
	coverage run -m pytest $(SOURCE_DIR)/tests; \
	coverage html

ifeq ($(OS),Windows_NT)
clean:
	-rmdir /s /q dist 2>nul
	-rmdir /s /q $(DOCS_DIR)\build 2>nul

else
clean:
	rm -rf dist \
	    $(DOCS_DIR)/build

endif

image: clean
	docker build -t $(DOCKERHUB_USER)/$(RELEASE_NAME):$(TAG) .

push: image
	docker push $(DOCKERHUB_USER)/$(RELEASE_NAME):$(TAG)

docker-compose-start:
	cd $(SCRIPT_DIR) && docker-compose up -d

deploy-k8s:
	kubectl apply -f $(SCRIPT_DIR)/k8s

doc:
	uv add -r $(DOCS_DIR)/requirements.txt --group docs
	sphinx-build -M html $(DOCS_DIR)/source/ $(DOCS_DIR)/build/

pypi:
	poetry build
	poetry publish
