#!/bin/bash

# PID=$(ps -elf | grep Qwen2.5-VL-32B-Instruct-AWQ | grep -v grep | awk '{print $4}')

PID=$(ps -elf | grep model-vllm-start | grep $1 | grep -v grep | awk '{print $4}')

echo "$PID"

SUBPID=$(ps -elf | awk -v pid=$PID '$5 == pid {print $4}')
SUBPIDLIST=$(ps -elf | awk -v pid=$SUBPID '$5 == pid {print $4}')

for pid in ${SUBPIDLIST[@]};do
	echo "$pid"
	kill -9 $pid
done

kill -9 $SUBPID
kill -9 $PID
