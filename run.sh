#!/bin/bash
exec poetry run python webservice.py &
exec poetry run python main.py