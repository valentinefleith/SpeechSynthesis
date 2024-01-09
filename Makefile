PYTHON = "python3"

SRC_DIR = "src"

.DEFAULT_GOAL = help

help:
	@echo "-------------------HELP-------------------"
	@echo "To download requirements type make setup"
	@echo "To run the project type make run"
	@echo "------------------------------------------"

run:
	@${PYTHON} ${SRC_DIR}/main.py

setup: requirements.txt
	pip install -r requirements.txt

pretty:
	@black ${SRC_DIR}

clean:
	@rm -rf ${SRC_DIR}/__pycache__
	@rm -rf utils/__pycache__
	@echo "All __pycache__ cleaned !"

.PHONY = help run setup pretty clean
