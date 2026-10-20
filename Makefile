PYTHON ?= python3

.PHONY: verify test contract
verify:
	$(PYTHON) tools/verify_snapshot.py

test:
	$(PYTHON) -m unittest discover -s tests -v

contract:
	cd contracts && npm run verify
