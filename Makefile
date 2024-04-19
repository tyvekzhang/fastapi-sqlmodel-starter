.PHONY: help install lint test start image push docker-compose-start deploy-k8s

tag = v1.0.0
releaseName = fastapi-sqlmodel-starter
dockerhubUser ?= tyvek2zhang


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
	@echo "Use 'make <target>' to run a specific command."

install:
	cd fss && \
	poetry shell && \
	poetry install

lint:
	python -m pip install pre-commit && \
	pre-commit run --all-files --verbose --show-diff-on-failure

test:
	cd fss && \
	alembic upgrade head && \
	coverage run -m pytest && \
	coverage html

start:
	cd fss && \
	python apiserver.py

image:
	docker build -t $(dockerhubUser)/$(releaseName):$(tag) .

push: image
	docker push $(dockerhubUser)/$(releaseName):$(tag)

docker-compose-start:
	cd deploy && \
	docker-compose up -d

deploy-k8s:
	kubectl apply -f deploy/k8s
