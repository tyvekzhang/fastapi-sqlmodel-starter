.PHONY: help install lint test start image push docker-compose-start deploy-k8s clean

tag = v1.0.0
releaseName = fastapi-sqlmodel-starter
dockerhubUser ?= tyvek2zhang
fssDir = fss
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
	@echo "  clean                 Remove temporary files."
	@echo "Use 'make <target>' to run a specific command."

install:
	cd $(fssDir) && \
	poetry shell && \
	poetry install

lint:
	python -m pip install pre-commit && \
	pre-commit run --all-files --verbose --show-diff-on-failure

test:
	cd $(fssDir) && \
	alembic upgrade head && \
	coverage run -m pytest && \
	coverage html

start:
	cd $(fssDir) && \
	alembic upgrade head && \
	python apiserver.py

image:
	docker build -t $(dockerhubUser)/$(releaseName):$(tag) .

push: image
	docker push $(dockerhubUser)/$(releaseName):$(tag)

docker-compose-start:
	cd ${deployDir} && \
	docker-compose up -d

deploy-k8s:
	kubectl apply -f ${deployDir}/k8s

clean:
	find . -type f -name '*.pyc' -delete; \
	find . -type d -name __pycache__ -delete; \
	rm -rf .pytest_cache; \
	rm -rf .ruff_cache; \
	rm -rf dist; \
	rm -rf poetry.lock; \
	rm -rf docs/build; \
	rm -rf $(fssDir)/htmlcov; \
	rm -rf $(fssDir)/.env_fss; \
	rm -rf $(fssDir)/.coverage; \
