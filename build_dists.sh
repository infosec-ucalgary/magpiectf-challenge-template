#!/bin/bash

for chall_dir in challenges/*/*/; do
    if [ -f "$chall_dir/Makefile" ]; then
        (cd "$chall_dir" && make dist)
    fi
done