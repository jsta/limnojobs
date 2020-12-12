install:
	pip install --upgrade -e .

run:
	python limnojobs/limnojobs.py --interactive

debug:
	python limnojobs/limnojobs.py --interactive --unseen

test:
	cd limnojobs && python -m pytest
