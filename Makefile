install:
	pip install --upgrade pip &&\
		pip install -r requirements/requirements.txt &&\
		pip install -r requirements/test_requirements.txt
format:
	black *.py
#lint:
#	pylint --disable=R,C *.py
#test:
#	python -m pytest 
all: install format