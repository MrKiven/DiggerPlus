clean-pyc:
	find . -type f -name '*.pyc' -exec rm -f {} +
	find . -type f -name '*.pyo' -exec rm -f {} +
	find . -type f -name '*.~' -exec rm -f {} +
	find . -type d -name '__pycache__' -exec rm -rf {} +

pep8:
	flake8 diggerplus tests

pylint: pep8
	bash tools/scripts/ci.sh

git-hooks:
	ln -sf `pwd`/tools/git-hooks/* .git/hooks/
