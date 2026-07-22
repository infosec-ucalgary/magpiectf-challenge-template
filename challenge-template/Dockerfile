# 1. Build Stage
FROM <BUILD_ENVIRONMENT> as builder
# Ex: FROM gcc:15 AS builder

WORKDIR /build
COPY src/ .

# Run all nessecary build commands here
# Ex: RUN gcc -o challenge_binary main.c

# 2. Compile all files that need to be distributed to the user
# Run `docker build --target dist --output type=local,dest=./dist .` to then populate the dist folder
FROM scratch AS dist
# Ex: COPY --from=builder /build/challenge_binary /challenge_binary

# 3. Runtime environment
FROM ubuntu:22.04
RUN apt-get update -y && apt-get install -y <DEPENDENCIES>

# Trim image of apt garbage
RUN rm -rf /var/lib/apt/lists/*

# Create underpriveleged user for challenge
RUN useradd -M -s /usr/sbin/nologin challuser

WORKDIR /chall

# Copy all required files to /chall
# Ex: COPY --from=builder /build/challenge_binary /chall/challenge_binary

COPY src/flag.txt /chall/flag.txt

# Limit permissions on challenge files
# Ex: RUN chmod 555 /chall/challenge_binary

RUN chmod 444 /chall/flag.txt

USER challuser

# Run final challenge
# Ex: CMD ["socat" "TCP-listen:1337,reuseaddr,fork", "EXEC:/chall/challenge_binary"]