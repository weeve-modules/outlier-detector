SHELL := /bin/bash

image:
	docker build -t sweeper .
.phony: image

run_image:
	docker run -p 8000:5000 --rm sweeper:latest
.phony: run_image

install_local:
	pip3 install -r requirements.txt
.phony: install_local

run_local:
	python3 sweeper.py --egress_api_host 0.0.0.0
.phony: run_local
