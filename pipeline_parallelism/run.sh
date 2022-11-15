#!/bin/bash

deepspeed train.py --deepspeed_config=ds_config.json -p 1 --steps=150
