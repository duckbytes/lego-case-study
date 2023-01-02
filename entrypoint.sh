#!/bin/bash

flask db upgrade
python -m pytest tests
python app.py
