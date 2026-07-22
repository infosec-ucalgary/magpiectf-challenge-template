#!/bin/bash
set -e

for chall_dir in challenges/*/*/; do
    if [ -f "$chall_dir/docker-compose.yml" ]; then
        echo "Deploying $chall_dir"
        (cd "$chall_dir" && docker compose up -d --build)
    fi
done