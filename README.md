# MagPieCTF Challenges Template

## Challenges
### Structure
```
challenge-name/
    dist/                          <- Files to be distributed to players
        ...
    src/                           <- Source code for building project
        ...
    challenge.yml                  <- Metadata to automate creation of challenges on CTFd
    docker-compose.yml             <- (Optional) Service file for rev/pwn/web challenges that need a server/website/binary running
    Dockerfile                     <- Build challenge and compile dist files 
    Makefile                       <- DO NOT ADD CUSTOM BUILD CODE HERE --- Used by scripts in root folder to populate dists and start challenges
    README.md                      <- Information about challenge
```
### Line-by-line File Explanations
<details>
<summary>`Dockerfile`</summary>

#### Build Image
This is the image your environment will be built in. There are many containers on [Docker Hub](https://hub.docker.com/search) that can be used to build your challenge. For example, if you are running a Node.JS server, the first line of your `Dockerfile` should look like:
```Dockerfile
FROM node:26 AS builder
```
or if you are compiling a C/C++ program, use `gcc:15` for example.
```Dockerfile
FROM gcc:15 AS builder
```
#### Installing dependencies
Next, install any build dependencies your challenge needs. For example, if it needs `make`, `libssl` and `python3`, make sure your Dockerfile looks like this
```Dockerfile
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends make libssl-dev python3 \
    && rm -rf /var/lib/apt/lists/*
```

#### Build File Setup
For the sake of consistency, all challenge builds will occur in the `/build` folder of the container and all source code files will be copied into it. DO NOT CHANGE THIS PART

```Dockerfile
WORKDIR /build
COPY src/ .
```

#### Building
Now, it is time to build your challenge. Run any and all build commands here. For example, if you need to run a `Makefile`, build an NPM project, or compile some C source code, do it here.

Compiling a C file
```Dockerfile
RUN gcc -o my_challenge_binary main.c
```

Building an NPM project
```Dockerfile
RUN npm build
```

#### Creating dist files
This is where you must copy all files that the player must recieve to finish the challenge. Note the following mandatory boilerplate:
```Dockerfile
FROM scratch AS dist
```
DO NOT MODIFY THIS PART

After that, you can copy your files to the root directory. For example, if you needed to distribute the binary we compiled in the previous step, use the following code:

```Dockerfile
COPY --from=builder /build/my_challenge_binary /my_challenge_binary
```

#### Runtime Setup
As of editing, we will be utilising Ubuntu 22.04 as our runtime environment. The following code snippet is nessecary boilerplate and should not be changed

```Dockerfile
FROM ubuntu:22.04
```

#### Installing runtime dependencies
Use the same command for installing build dependencies for installing the runtime dependencies. For example, if we require `socat` to give access to a binary to the user, use the following command:
```Dockerfile
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*
```

#### Unpriveleged User Creation
We don't want our runtime environment getting nuked by some cheeky player if they manage to connect to it. So, each challenge will be running as an underpriveleged user who can't really mess anything up
```Dockerfile
RUN useradd -M -s /usr/sbin/nologin challuser
```

#### Runtime File Setup
All runtime files will be in `/chall`
```Dockerfile
WORKDIR /chall
```
All files that are required to run your program should be moved here from `/build`. For example, if you had the C binary from before and needed to run it, use the following command:
```Dockerfile
COPY --from=builder /build/my_challenge_binary /chall/my_challenge_binary
```
Do the same for any other file needed to run your challenge. Do not forget to copy the `flag.txt` as well
```Dockerfile
COPY src/flag.txt /chall/flag.txt
```

#### Permission hardening
For anything that must be executable, please set the permisisons to 555 and for anything that does not need to be executable, please set the permission to 444. Continuing our previous example, `my_challenge_binary` must be executable so we set it to 555 and flag.txt does not so it will be 444

```Dockerfile
RUN chmod 555 /chall/my_challenge_binary
RUN chmod 444 /call/flag.txt
```

#### Starting challenge
The challenge should be run by our underpriveleged user:
```Dockerfile
USER challuser
```

Then the actual command that starts the challenge. For example, to give the players access to our previous example's `my_challenge_binary`, we use the following command:

```Dockerfile
CMD ["socat" "TCP-listen:1337,reuseaddr,fork", "EXEC:/chall/my_challenge_binary"]
```

</details>

<details>
<summary>`docker-compose.yml`</summary>

This file will be responsible for running your challenge, if nessecary (primarily for PWN and WEB challenges that require some sort of server). Simply fill in the challenge name and adjust the port as nessecary.

</details>

</details>

<details>
<summary>`compose.yml`</summary>

This file will contain metadata that will be used by the CTFd instance to populate the challenges automatically

<!-- TODO: Add more details -->

</details>

<details>
<summary>`Makefile`</summary>

DO NOT MODIFY THIS FILE (besides adding the challenge name). You are free to use a `Makefile` yourself in your source code, just make sure not to touch this file and if you do need a `Makefile` in your source code, be sure to run it in the `Dockerfile`.

</details>




## Deploying
- `build_dists.sh` will populate the `dist` folder of each challenge as nessecary
- `start_challenges.sh` will start each challenge's container if there is a `docker-compose.yml` in it
- `push_challenges.py` will interact with the CTFd API to update the challenges listed on it. Ensure environment variables `CTFD_URL` and `CTFD_TOKEN` exist in production