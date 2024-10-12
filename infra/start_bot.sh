#!/usr/bin/env bash

cd /home/ec2-user/pushup/
export LOG_LEVEL="ERROR"
export PYTHONPATH=${PYTHONPATH}:.
source .venv/bin/activate
python bot/cody.py
