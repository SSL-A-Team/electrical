#!/usr/bin/env bash

export REPO_ROOT=$(realpath ./.)

# Python configs
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

# Poetry configs
export POETRY_VIRTUALENVS_CREATE=true
export POETRY_VIRTUALENVS_IN_PROJECT=true
export POETRY_VIRTUALENVS_PROMPT="ateam-elec"

# Load into the shell
if command -v poetry &> /dev/null; then
	poetry install
	source $REPO_ROOT/.venv/bin/activate
fi
