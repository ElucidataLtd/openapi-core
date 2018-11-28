.PHONY: build

help: ## Prints this help/overview message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-17s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Creates a new build for publishing. Deletes previous builds.
	rm -rf build/* dist/*
	pip install -U setuptools wheel
	python setup.py sdist bdist_wheel

publish: ## Publishes 1 build package to users default PyPi server specified in .pypirc
	twine upload dist/*
