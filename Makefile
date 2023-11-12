BUILD_DIR = ./src

PYTHON = python

# Style
style:
	black .
	flake8 ${BUILD_DIR}
	${PYTHON} -m isort ${BUILD_DIR}
