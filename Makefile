PYTHON         := /usr/bin/env python3
VERSION_FILE 	= ./tycho/__init__.py
VERSION      	= $(shell cut -d " " -f 3 ${VERSION_FILE})
REGISTRY 		= docker.io
APP_OWNER 		= helxplatform
APP_NAME	 	= tycho-api
IMAGE_NAME	 	= ${APP_OWNER}/${APP_NAME}
IMAGE_TAG   	= "${VERSION}-${BUILD_NUMBER}"

.DEFAULT_GOAL = help

.PHONY: help clean install test build image publish

version:
	${PYTHON} --version
	echo ${VERSION}
#help: List available tasks on this project
help:
	@grep -E '^#[a-zA-Z\.\-]+:.*$$' $(MAKEFILE_LIST) | tr -d '#' | awk 'BEGIN {FS = ": "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean:
	${PYTHON} -m pip uninstall -y tycho-api
	${PYTHON} -m pip uninstall -y -r requirements.txt

install:
	${PYTHON} -m pip install --upgrade pip
	${PYTHON} -m pip install --upgrade wheel
	${PYTHON} -m pip install --upgrade setuptools
	${PYTHON} -m pip install -r requirements.txt
	${PYTHON} -m pip install .

#test: Run all tests
test:
	# ${PYTHON} -m flake8 src
	${PYTHON} -m pytest tests

buildAndPush:
	/kaniko/executor --dockerfile Dockerfile --context . --verbosity debug --destination ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
