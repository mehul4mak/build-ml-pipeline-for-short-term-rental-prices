lint:
	pylint *.py */*/*.py


format:
	autopep8 --in-place --aggressive --aggressive main.py
	autopep8 --in-place --aggressive --aggressive src/*/*.py

pytest:



all:
	lint
	format
	pytest