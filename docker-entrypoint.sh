#!/bin/sh

# exit from script if error was raised.
set -e

echo "Command: python -m lightning_rest.server $@"

exec python -m lightning_rest.server "$@"
