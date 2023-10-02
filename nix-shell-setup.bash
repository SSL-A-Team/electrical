#!/usr/bin/env bash

export REPO_ROOT=$(realpath ./.)

export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring

export POETRY_VIRTUALENVS_CREATE=true
export POETRY_VIRTUALENVS_IN_PROJECT=true
export POETRY_VIRTUALENVS_PROMPT="ateam-elec"

if command -v poetry &> /dev/null; then
	poetry install
	source $REPO_ROOT/.venv/bin/activate
fi
