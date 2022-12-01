all: run

install:
	pip install --upgrade -e .

run:
	python limnojobs/limnojobs.py --interactive

debug:
	python limnojobs/limnojobs.py --interactive --unseen

test:
	cd limnojobs && python -m pytest

keywords:
	git pull && git add limnojobs/keywords.csv && git commit -m "stash keywords [skip ci]" && git push

log:
	git pull && git add log.csv && git commit -m "stash log [skip ci]" && git push
