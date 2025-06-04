.PHONY: help install lint test start image push docker-compose-start deploy-k8s doc pypi clean

tag ?= v1.1.1
releaseName = fast-web
dockerhubUser = tyvek2zhang
homeDir = src
deployDir = deploy

help:
	@echo "Available make targets:"
	@echo "  install               Install project dependencies using uv."
	@echo "  db                    Generate db structure."
	@echo "  dp                    Upgrade db structure."
	@echo "  dev                   Development environment startup."
	@echo "  start                 Production environment startup."
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
	@echo "Use 'make <target>' to run a specific command."

install:
	uv sync

db:
	alembic revision --autogenerate

dp:
	alembic upgrade head

dev:
	alembic upgrade head && \
	uv run apiserver.py

start:
	alembic upgrade head && \
	nohup alembic upgrade head && uvicorn apiserver.py --env prod > server.log 2>&1 &

lint:
	uv add pre-commit --group test && \
	pre-commit run --all-files --verbose --show-diff-on-failure

test:
	rm -rf src/main/resource/alembic/db/fast_web.db; \
	rm -rf htmlcov; \
	uv sync --group dev ; \
	alembic upgrade head; \
	coverage run -m pytest src/tests; \
	coverage html

clean:
	rm -rf dist; \
	rm -rf .pytest_cache; \
	rm -rf .ruff_cache; \
	rm -rf log; \
	rm -rf docs/build; \
	rm -rf $(homeDir)/htmlcov; \
	rm -rf $(homeDir)/migrations/db/fast_web.db; \
	rm -rf $(homeDir)/.env_fast_web; \
	rm -rf $(homeDir)/.coverage;

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
