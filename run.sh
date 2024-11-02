#!/bin/bash
set -e
service ssh start
exec poetry run python webservice.py &
exec poetry run python main.py