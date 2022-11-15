#!/bin/bash

# deepspeed --hostfile=hostfile train.py --deepspeed_config=ds_config.json -p 2 --steps=150
# deepspeed --include="127.0.0.1:0@127.0.0.1:1" train.py --deepspeed_config=ds_config.json -p 2 --steps=150
