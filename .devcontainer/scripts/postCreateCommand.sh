#!/usr/bin/env bash

echo "Making sure the source and cache directory is owned by vscode..."
sudo chown -R vscode:vscode /home/vscode/.cache

echo "Installing pre-commit hooks..."
pre-commit install --install-hooks
