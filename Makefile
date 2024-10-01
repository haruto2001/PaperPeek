.PHONY: build run check format isort

IMAGE_NAME = "paper-peek"
UBUNTU_VERSION = "22.04"
USERNAME = "user"
WORKDIR = "/work"


build: ./Dockerfile ./entrypoint.sh
	docker build . \
	-t $(IMAGE_NAME) \
	--build-arg CONTAINER_VERSION=$(CONTAINER_VERSION) \
	--build-arg USERNAME=$(USERNAME) \
	--build-arg WORKDIR=$(WORKDIR)

run:
	docker run -it --rm \
	-e LOCAL_UID=$(shell id -u $(USER)) \
	-e LOCAL_GID=$(shell id -g $(USER)) \
	--mount type=bind,src=.,dst=/work \
	$(IMAGE_NAME) bash

check: ./src
	uv run ruff check ./src

format: ./src
	uv run ruff format --diff ./src

isort: ./src
	uv run isort --diff ./src