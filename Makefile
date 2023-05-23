, := ,

# --- Docker
image_name := collab/core
docker_image := $(image_name):latest
lambda_image := $(image_name):ci

# --- Compose
DOCKER_COMPOSE_FILE ?= docker-compose.yml
compose := docker compose -f $(DOCKER_COMPOSE_FILE)
profile ?= collab

ifeq (,$(wildcard /.dockerenv))
	exec := $(compose) exec django
	tty := t
endif

# --- Django
manage := $(exec) python manage.py
django_locales := tr

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build          Build docker image"
	@echo "  up             Run the docker containers and build the images"
	@echo "  logs           View output from docker containers"
	@echo "  sh             Run bash shell on the app container"
	@echo "  shell          Start the Python interactive interpreter"
	@echo "  check          Inspect the entire Django project for common problems"
	@echo "  migrate        Update database schema"
	@echo "  migration      Make migration and migrate shortcut"
	@echo "  static         Collect the static files into STATIC_ROOT"

build:
	@DOCKER_BUILDKIT=1 docker build \
		-t $(docker_image) .

build.if:
	@if [ "$$(docker images -q $(docker_image) 2> /dev/null)" == "" ]; then \
		$(MAKE) -s build; \
	fi

up: build.if
	@$(compose) --profile $(profile) up -d

logs:
	@$(compose) --profile $(profile) logs -f

sh:
	@$(exec) /bin/bash

shell:
	@$(manage) shell_plus --quiet-load

check:
	@$(manage) check

makemigrations:
	@$(manage) makemigrations

migrate:
	@$(manage) migrate

static:
	@$(manage) collectstatic

lambda:
	@DOCKER_BUILDKIT=1 docker build \
		-t $(lambda_image) -f lambda/Dockerfile .

test:
	@$(exec) pytest

show-packages:
	@$(exec) pip freeze

flake8:
	@$(exec) flake8

isort:
	@$(exec) isort -c .

bandit:
	@$(exec) bandit -r .

coverage:
	@$(exec) pytest $(options) \
		--cov=. \
		--cov-report term \
		--cov-report html

ci:
	@$(compose) up -d
	$(compose) exec -T django /bin/bash -c \
		'source /entrypoint && make coverage flake8 isort bandit'

.PHONY: help build build.if up logs sh shell check makemigrations migrate static lambda test flake8 isort bandit coverage ci
