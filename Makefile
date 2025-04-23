.PHONY: help install lint test start image push docker-compose-start deploy-k8s doc pypi clean

tag ?= v1.1.1
releaseName = fastapi-sqlmodel-starter
dockerhubUser = tyvek2zhang
homeDir = src
deployDir = deploy

help:
	@echo "Available make targets:"
	@echo "  install               Install project dependencies using poetry."
	@echo "  lint                  Perform static code analysis."
	@echo "  test                  Run unit tests."
	@echo "  start                 Start the project."
	@echo "  image                 Build the Docker image for the project."
	@echo "  push                  Push Docker image to dockerHub."
	@echo "  docker-compose-start  Start the project using Docker Compose."
	@echo "  deploy-k8s            Deploy the project to Kubernetes."
	@echo "  doc                   Make doc for this project."
	@echo "  pypi                  Build and publish to pypi."
	@echo "  clean                 Remove temporary files."
	@echo "  db                    Generate db structure."
	@echo "  db_up                 Upgrade db structure."
	@echo "Use 'make <target>' to run a specific command."

install:
	@echo "Detecting OS..."
ifeq ($(OS),Windows_NT)
	@echo "Windows system detected"
	uv venv --python 3.11 && .venv\Scripts\activate && uv sync
else
	@echo "Linux/Mac system detected"
	uv venv --python 3.11 && . .venv/bin/activate && uv sync
endif

db:
	alembic revision --autogenerate

db_up:
	alembic upgrade head

lint:
	uv add pre-commit --group test && \
	pre-commit run --all-files --verbose --show-diff-on-failure

test:
	rm -rf src/main/resource/alembic/db/fss.db; \
	rm -rf htmlcov; \
	uv sync --group dev ; \
	alembic upgrade head; \
	coverage run -m pytest src/tests; \
	coverage html

start:
	alembic upgrade head && \
	python src/apiserver.py

clean:
	find . -type f -name '*.pyc' -delete; \
	find . -type d -name __pycache__ -delete; \
	rm -rf .pytest_cache; \
	rm -rf .ruff_cache; \
	rm -rf dist; \
	rm -rf log; \
	rm -rf poetry.lock; \
	rm -rf docs/build; \
	rm -rf $(homeDir)/htmlcov; \
	rm -rf $(homeDir)/migrations/db/fss.db; \
	rm -rf $(homeDir)/.env_fss; \
	rm -rf $(homeDir)/.coverage; \

image: clean
	docker build -t $(dockerhubUser)/$(releaseName):$(tag) .

push: image
	docker push $(dockerhubUser)/$(releaseName):$(tag)

docker-compose-start:
	cd ${deployDir} && \
	docker-compose up -d

deploy-k8s:
	kubectl apply -f ${deployDir}/k8s

doc:
	pip install -r docs/requirements.txt; \
	sphinx-build -M html docs/source/ docs/build/

pypi:
	poetry build; \
	poetry publish
